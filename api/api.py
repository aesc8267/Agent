from flask import Flask, request, jsonify, blueprints
import os
from models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, insert, delete
from sqlalchemy.exc import SQLAlchemyError
from flask_docs import ApiDoc
from flask_cors import CORS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
CORS(app, origins='*')
engine = create_engine('mysql+pymysql://root:root@localhost/agent')
DBSession = sessionmaker(bind=engine)
# 自动生成请求参数 markdown
# app.config["API_DOC_AUTO_GENERATING_ARGS_MD"] = True
# # 允许显示的方法
# app.config["API_DOC_METHODS_LIST"] = ["GET", "POST", "PUT", "DELETE", "PATCH"]
app.config["API_DOC_MEMBER"] = ["api"]
ApiDoc(
    app,
    title="Sample App",
    version="1.0.0",
    description="A simple app API",
)

api = blueprints.Blueprint('api', __name__)


@api.route('/users/register', methods=['POST'])
def register():
    """
        ### args
        |  args | required | request type | type |  remarks |
        |-------|----------|--------------|------|----------|
        | username |  true    |    body      | str  | user name  |
        | password  |  true    |    body      | str  | user password |

        ### request
        ```json
        {"username": "xxx", "password": "xxx"}
        ```

        ### return
        ```json
        {"code": 200, "msg": "Success", "data": null}
        ```
        """
    db = DBSession()
    try:
        data = request.get_json()
        username = data.get('username')
        # email = data.get('email')
        password = data.get('password')  # 记得在生产环境中进行密码加密处理
        new_user = Users(username=username, password=password)
        db.add(new_user)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        return 'Error', 500
    db.close()
    return 'Success', 200


@api.route('/users/login', methods=['POST'])
def login():
    pass


@api.route('/users/profile', methods=['GET'])
def get_profile():
    pass


@api.route('/agents/add', methods=['POST'])
def add_agent():
    """
    ### args
    |  args | required | request type | type |  remarks |
    |-------|----------|--------------|------|----------|
    | name  |  true    |    body      | str  | agent name |
    | description  |  true    |    body      | str  | agent description |
    | llm_id  |  true    |    body      | int  | llm id |
    ### request
    ```json
    { "name": "xxx", "description": "xxx", "llm_id": 'xxx'}
    ```
    ### return
    ```json
    {"message": "Agent created", "agent_id": 1}
    ```
    """
    db = DBSession()
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        name = data.get('name')
        description = data.get('description')
        llm_id = data.get('llm_id')
        new_agent = Agents(agent_name=name, agent_description=description, llm_id=llm_id)
        db.add(new_agent)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        return 'Error', 500
    try:
        # 如果传入工具ID列表，则建立关联
        tools = data.get('tools', [])
        for tool_id in tools:
            agent_tool = insert(t_agent_tools).values(agent_id=new_agent.agent_id, tool_id=tool_id)
            db.execute(agent_tool)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        return 'Error', 500
    return jsonify({'message': 'Agent created', 'agent_id': new_agent.agent_id}), 200


@api.route('/agents/list')
def list_agents():
    """ get all agents
    ### args
    None
    ### return
    ```json
    [
    {
    "agent_id": xxx,
    "name": "xxx",
    "description": "xxx",
    "llm_id": xxx,
    "update_time": "xxx"

    }
    ]
    ```
    """
    db = DBSession()
    try:
        agents = db.query(Agents).all()
        result = []
        for agent in agents:
            result.append({
                'agent_id': agent.agent_id,
                'name': agent.agent_name,
                'description': agent.agent_description,
                'llm_id': agent.llm_id,
                'update_time': agent.update_time
            })
            # tools=db.query(t_agent_tools).filter(t_agent_tools.c.agent_id == agent.agent_id).all()
            # for tool in tools:
            #     result[-1]['tools'].append(db.query(Tools).filter(Tools.tool_id == tool.tool_id).first().tool_name)
            #
    except SQLAlchemyError as e:
        print(e)
        return 'Error', 500
    return jsonify(result), 200


@api.route('/agents/delete/<agent_id>/')
def delete_agent(agent_id):
    """ delete agent by id
    ### args
    |  args | required | request type | type |  remarks |
    |-------|----------|--------------|------|----------|
    | agent_id |  true    |    query      | int  | agent id |
    ### return
    ```json
    {"message": "Agent deleted"}
    ```
    """
    db = DBSession()
    try:
        agent = db.query(Agents).filter(Agents.agent_id == agent_id).first()  # 先查询再delete 保证级联删除
        db.delete(agent)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        return 'Error', 500
    return jsonify({'message': 'Agent deleted'}), 200


@api.route('/agents/get/<agent_id>/')
def get_agent(agent_id):
    """ get agent by id
    ### args
    |  args | required | request type | type |  remarks |
    |-------|----------|--------------|------|----------|
    | agent_id |  true    |    query      | int  | agent id |
    ### return
    ```json
    {
    "agent_id": xxx,
    "name": "xxx",
    "description": "xxx",
    "llm_id": xxx,
    "update_time": "xxx"
    }
    """
    db = DBSession()
    try:
        agent = db.query(Agents).filter(Agents.agent_id == agent_id).first()
        result = {
            'agent_id': agent.agent_id,
            'name': agent.agent_name,
            'description': agent.agent_description,
            'llm_id': agent.llm_id,
            'update_time': agent.update_time
        }
        tools = db.query(t_agent_tools).filter(t_agent_tools.c.agent_id == agent_id).all()
        result['tools'] = []
        for tool in tools:
            result['tools'].append(db.query(Tools).filter(Tools.tool_id == tool.tool_id).first().tool_name)
    except SQLAlchemyError as e:
        print(e)
        return 'Error', 500
    return jsonify(result), 200

@api.route('/agents/update', methods=['post'])
def update_agent():
    """
    ## args
    |  args | required | request type | type |  remarks |
    |-------|----------|--------------|------|----------|
    | agent_id |  true    |    body      | int  | agent id |
    | name |  true    |    body      | str  | agent name |
    | description |  true    |    body      | str  | agent description |
    | llm_id |  true    |    body      | int  | llm id |
    ### request
    ```json
    { "agent_id": "xxx", "name": "xxx", "description": "xxx", "llm_id": "xxx"}
    ```
    ### return
    ```json
    {"message": "Agent updated", "agent_id": 1}
    """
    db = DBSession()
    try:
        data = request.get_json()
        agent_id = data.get('agent_id')
        name = data.get('name')
        description = data.get('description')
        llm_id = data.get('llm_id')
        agent = db.query(Agents).filter(Agents.agent_id == agent_id).first()
        agent.agent_name = name
        agent.agent_description = description
        agent.llm_id = llm_id
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        return 'Error', 500
    return jsonify({'message': 'Agent updated', 'agent_id': agent_id}), 200
@api.route('/agent_tools/add', methods=['post'])
def add_agent_tools():
    """
    ## args
    |  args | required | request type | type |  remarks |
    |-------|----------|--------------|------|----------|
    | agent_id |  true    |    body      | int  | agent id |
    | tools |  true    |    body      | list  | tool id list |
    ### request
    ```json
    { "agent_id": "xxx", "tools": ["xxx", "xxx"]}
    ```
    ### return
    ```json
    {"message": "tools created", "agent_id": 1}
    ```
    """
    db = DBSession()
    try:
        data = request.get_json()
        agent_id = data.get('agent_id')
        tools = data.get('tools', [])
        for tool_id in tools:
            agent_tool = insert(t_agent_tools).prefix_with("IGNORE").values(agent_id=agent_id, tool_id=tool_id)
            db.execute(agent_tool)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        return 'Error', 500
    return jsonify({'message': 'tools created', 'agent_id': agent_id}), 200


@api.route('/agent_tools/get/<agent_id>/', methods=['GET'])
def get_agent_tools(agent_id):
    """ get  agent tools by agent_id
    ### args
    |  args | required | request type | type |  remarks |
    |-------|----------|--------------|------|----------|
    | agent_id |  true    |    query      | int  | agent id |
    ### return
    ```json
    [
    {
    "agent_id": xxx,
    "tool_id": xxx
    }
    ]
    ```
    """
    db = DBSession()
    try:
        agent_tools = db.query(t_agent_tools).filter(t_agent_tools.c.agent_id == agent_id).all()
        result = []
        for agent_tool in agent_tools:
            result.append({
                'agent_id': agent_tool.agent_id,
                'tool_id': agent_tool.tool_id
            })
    except SQLAlchemyError as e:
        print(e)
        return 'Error', 500
    return jsonify(result), 200


@api.route('/agent_tools/delete/<agent_id>/', methods=['post'])
def delete_agent_tools(agent_id):
    """ delete agent tools by agent_id
    ### args
    |  args | required | request type | type |  remarks |
    |-------|----------|--------------|------|----------|
    | agent_id |  true    |    query      | int  | agent id |
    ### return
    ```json
    {"message": "tools deleted"}
    ```
    """
    db = DBSession()
    try:
        sql = delete(t_agent_tools).where(t_agent_tools.c.agent_id == agent_id)
        db.execute(sql)  # 删除指定agent_id的所有记录,不需要考虑级联关系
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        return 'Error', 500
    return jsonify({'message': 'tools deleted'}), 200


# 获取所有工具（包含预定义和用户自定义）
@api.route('/tools/list', methods=['GET'])
def get_tools():
    """ get all tools
    ### args
    None
    ### return
    ```json
    [
    {
    "tool_id": xxx,
    "name": "xxx",
    "description": "xxx",
    "inputs": "xxx",
    "output_type": "xxx",
    "update_time": "xxx"
    ```
    """
    db = DBSession()
    tools = db.query(Tools).all()
    result = []
    for tool in tools:
        result.append({
            'tool_id': tool.tool_id,
            'name': tool.tool_name,
            'description': tool.tool_description,
            'inputs': tool.inputs,
            'output_type': tool.output_type,
            'update_time': tool.update_time
        })
    return jsonify(result), 200


# 用户自定义工具上传（工具文件以 Python 文件或者粘贴python 代码形式上传）
@api.route('/tools/add', methods=['POST'])
def add_tool():
    """ Content-Type=form-data
    ### args
    |  args | required | request type | type |  remarks |
    |-------|----------|--------------|------|----------|
    | name  |  true    |    body      | str  | tool name |
    | description  |  true    |    body      | str  | tool description |
    | inputs  |  true    |    body      | str  | tool inputs |
    | output_type  |  true    |    body      | str  | tool output type |
    | code  |  true    |    body      | str  | tool code or can upload by file|
    ### request
    ```json
    { "name": "xxx", "description": "xxx", "inputs": "xxx", "output_type": "xxx", "code": "xxx"}
    ```
    ### return
    ```json
    {"message": "Tool created", "tool_id": 1}
    ```
    """
    user_id = request.form.get('user_id')
    name = request.form.get('name')
    description = request.form.get('description')
    inputs = request.form.get('inputs')
    output_type = request.form.get('output_type')
    code = request.form.get('code')
    # 通过表单上传的文件
    file = request.files.get('file')
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    elif code:
        filename = name + '.py'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            return jsonify({'error': 'tool already exists'}), 400
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
        except Exception as e:
            print(e)
            return jsonify({'error': 'Failed to save file'}), 500
    else:
        return jsonify({'error': 'No code uploaded'}), 400

    new_tool = Tools(user_id=1, tool_name=name, tool_description=description, inputs=inputs, output_type=output_type)
    db = DBSession()
    try:
        db.add(new_tool)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        return 'Error', 500
    return jsonify({'message': 'Tool created', 'tool_id': new_tool.tool_id, 'file_path': file_path}), 200


@api.route('/tools/delete/<tool_id>', methods=['POST'])
def delete_tool(tool_id):
    """
    ### args
    |  args | required | request type | type |  remarks |
    |-------|----------|--------------|------|----------|
    | tool_id |  true    |    query      | int  | tool id |
    ### return
    ```json
    {"message": "Tool deleted"}
    ```
    """
    db = DBSession()
    try:
        tool = db.query(Tools).filter(Tools.tool_id == tool_id).first()
        if tool:
            db.delete(tool)
            db.commit()
            return jsonify({'message': 'Tool deleted'}), 200
        else:
            return jsonify({'error': 'Tool not found'}), 404
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        return 'Error', 500


# 获取大模型列表
@api.route('/llms/list', methods=['GET'])
def list_llm():
    """ get all llms
    ### args
    None
    ### return
    ```json
    [
    {
    "llm_id": xxx,
    "name": "xxx",
    "api_key": "xxx",
    "base_url": "xxx",
    "update_time": "xxx"
    }
    ]
    ```
    """
    db = DBSession()
    llms = db.query(Llms).all()
    result = []
    for llm in llms:
        result.append({
            'llm_id': llm.llm_id,
            'llm_name': llm.llm_name,
            'api_key': llm.api_key,
            'base_url': llm.base_url,
            'update_time': llm.update_time
        })
    return jsonify(result)


# 创建大模型（支持用户自定义）
@api.route('/llm/add', methods=['POST'])
def add_llm():
    """ Content-Type=form-data
    ### args
    |  args | required | request type | type |  remarks |
    |-------|----------|--------------|------|----------|
    | name  |  true    |    body      | str  | llm name |
    | api_key  |  true    |    body      | str  | llm api key |
    | base_url  |  true   |    body      | str  | llm base url |
    ### request
    ```json
    { "name": "xxx", "api_key": "xxx", "base_url": "xxx"}
    ```
    ### return
    ```json
    {"message": "LLM created", "llm_id": 1}
    """
    data = request.get_json()
    # user_id = data.get('user_id')
    llm_name = data.get('name')
    api_key = data.get('api_key')
    base_url = data.get('base_url')
    new_llm = Llms(llm_name=llm_name, api_key=api_key, base_url=base_url)
    db = DBSession()
    try:
        db.add(new_llm)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        return 'error', 400
    return jsonify({'message': 'LLM created', 'llm_id': new_llm.llm_id}), 200


# 用户文件上传接口（图片、CSV、其他文件）
@api.route('/files/upload', methods=['POST'])
def upload_file():
    """ Content-Type=form-data
    ### args
    |  args | required | request type | type |  remarks |
    |-------|----------|--------------|------|----------|
    | file  |  true    |    body      | file  | file |
    ### request
    ```json
    {"file_type": "xxx", "file": "xxx"}
    ```
    ### return
    ```json
    {"message": "File uploaded", "file_id": 1, "file_path": "xxx"}
    ```
    """
    db = DBSession()
    # user_id = request.form.get('user_id')
    # file_type = request.form.get('file_type')  # 应为 'image', 'csv' 或 'file'
    file = request.files.get('file')
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        new_file = Files(user_id=1, file_name=filename, file_path=file_path)
        try:
            db.add(new_file)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            print(e)
            return 'Error', 500
        return jsonify({'message': 'File uploaded', 'file_id': new_file.file_id, 'file_path': file_path})
    else:
        return jsonify({'error': 'No file uploaded'}), 400


app.register_blueprint(api, url_prefix='/v1')

# ------------------------
# 启动程序
# ------------------------
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
