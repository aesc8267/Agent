from typing import List, Optional

from sqlalchemy import Column, DateTime, ForeignKeyConstraint, Index, Integer, String, Table, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Llms(Base):
    __tablename__ = 'llms'

    llm_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    llm_name: Mapped[str] = mapped_column(String(255))
    api_key: Mapped[str] = mapped_column(String(255))
    base_url: Mapped[str] = mapped_column(String(255))
    update_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    agents: Mapped[List['Agents']] = relationship('Agents', back_populates='llm')


class Users(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(256))
    role: Mapped[str] = mapped_column(String(20))
    create_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    charts: Mapped[List['Charts']] = relationship('Charts', back_populates='user')
    files: Mapped[List['Files']] = relationship('Files', back_populates='user')
    logs: Mapped[List['Logs']] = relationship('Logs', back_populates='user')
    rag_docs: Mapped[List['RagDocs']] = relationship('RagDocs', back_populates='user')
    tools: Mapped[List['Tools']] = relationship('Tools', back_populates='user')
    conversations: Mapped[List['Conversations']] = relationship('Conversations', back_populates='user')
    messages: Mapped[List['Messages']] = relationship('Messages', back_populates='user')


class Agents(Base):
    __tablename__ = 'agents'
    __table_args__ = (
        ForeignKeyConstraint(['llm_id'], ['llms.llm_id'], name='agents_ibfk_1'),
        Index('llm_id', 'llm_id')
    )

    agent_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    agent_name: Mapped[str] = mapped_column(String(255))
    agent_description: Mapped[str] = mapped_column(String(255))
    llm_id: Mapped[int] = mapped_column(Integer)
    create_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    llm: Mapped['Llms'] = relationship('Llms', back_populates='agents')
    tool: Mapped[List['Tools']] = relationship('Tools', secondary='agent_tools', back_populates='agent')
    agent_pakages: Mapped[List['AgentPakages']] = relationship('AgentPakages', back_populates='agent')
    conversations: Mapped[List['Conversations']] = relationship('Conversations', back_populates='agent')
    messages: Mapped[List['Messages']] = relationship('Messages', back_populates='agent')


class Charts(Base):
    __tablename__ = 'charts'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='charts_ibfk_1'),
        Index('user_id', 'user_id')
    )

    chart_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    chart_type: Mapped[str] = mapped_column(String(50))
    data_source: Mapped[str] = mapped_column(String(255))
    create_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    user: Mapped['Users'] = relationship('Users', back_populates='charts')


class Files(Base):
    __tablename__ = 'files'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='files_ibfk_1'),
        Index('user_id', 'user_id')
    )

    file_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(255))
    upload_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    user: Mapped['Users'] = relationship('Users', back_populates='files')
    message: Mapped[List['Messages']] = relationship('Messages', secondary='message_files', back_populates='file')


class Logs(Base):
    __tablename__ = 'logs'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='logs_ibfk_1'),
        Index('user_id', 'user_id')
    )

    log_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    operation_type: Mapped[str] = mapped_column(String(50))
    operation_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    user: Mapped['Users'] = relationship('Users', back_populates='logs')


class RagDocs(Base):
    __tablename__ = 'rag_docs'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='rag_docs_ibfk_1'),
        Index('user_id', 'user_id')
    )

    doc_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    doc_name: Mapped[str] = mapped_column(String(255))
    doc_path: Mapped[str] = mapped_column(String(255))
    create_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    user: Mapped['Users'] = relationship('Users', back_populates='rag_docs')


class Tools(Base):
    __tablename__ = 'tools'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='tools_ibfk_1'),
        Index('user_id', 'user_id')
    )

    tool_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    tool_name: Mapped[str] = mapped_column(String(255))
    tool_description: Mapped[Optional[str]] = mapped_column(Text)
    update_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    inputs: Mapped[Optional[str]] = mapped_column(Text)
    output_type: Mapped[Optional[str]] = mapped_column(Text)

    agent: Mapped[List['Agents']] = relationship('Agents', secondary='agent_tools', back_populates='tool')
    user: Mapped['Users'] = relationship('Users', back_populates='tools')


class AgentPakages(Base):
    __tablename__ = 'agent_pakages'
    __table_args__ = (
        ForeignKeyConstraint(['agent_id'], ['agents.agent_id'], name='agent_pakages_ibfk_1'),
    )

    agent_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pakage_name: Mapped[str] = mapped_column(String(255), primary_key=True)

    agent: Mapped['Agents'] = relationship('Agents', back_populates='agent_pakages')


t_agent_tools = Table(
    'agent_tools', Base.metadata,
    Column('agent_id', Integer, primary_key=True, nullable=False),
    Column('tool_id', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['agent_id'], ['agents.agent_id'], name='agent_tools_ibfk_1'),
    ForeignKeyConstraint(['tool_id'], ['tools.tool_id'], name='agent_tools_ibfk_2'),
    Index('tool_id', 'tool_id')
)


class Conversations(Base):
    __tablename__ = 'conversations'
    __table_args__ = (
        ForeignKeyConstraint(['agent_id'], ['agents.agent_id'], name='conversations_ibfk_2'),
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='conversations_ibfk_1'),
        Index('agent_id', 'agent_id'),
        Index('user_id', 'user_id')
    )

    conversation_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    agent_id: Mapped[int] = mapped_column(Integer)
    conversation_name: Mapped[str] = mapped_column(String(255))
    create_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    agent: Mapped['Agents'] = relationship('Agents', back_populates='conversations')
    user: Mapped['Users'] = relationship('Users', back_populates='conversations')
    messages: Mapped[List['Messages']] = relationship('Messages', back_populates='conversation')


class Messages(Base):
    __tablename__ = 'messages'
    __table_args__ = (
        ForeignKeyConstraint(['agent_id'], ['agents.agent_id'], name='messages_ibfk_3'),
        ForeignKeyConstraint(['conversation_id'], ['conversations.conversation_id'], name='messages_ibfk_1'),
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='messages_ibfk_2'),
        Index('agent_id', 'agent_id'),
        Index('conversation_id', 'conversation_id'),
        Index('user_id', 'user_id')
    )

    message_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    conversation_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)
    agent_id: Mapped[int] = mapped_column(Integer)
    agent_content: Mapped[str] = mapped_column(Text)
    user_content: Mapped[str] = mapped_column(Text)
    create_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    file: Mapped[List['Files']] = relationship('Files', secondary='message_files', back_populates='message')
    agent: Mapped['Agents'] = relationship('Agents', back_populates='messages')
    conversation: Mapped['Conversations'] = relationship('Conversations', back_populates='messages')
    user: Mapped['Users'] = relationship('Users', back_populates='messages')


t_message_files = Table(
    'message_files', Base.metadata,
    Column('file_id', Integer, primary_key=True, nullable=False),
    Column('message_id', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['file_id'], ['files.file_id'], name='message_files_ibfk_1'),
    ForeignKeyConstraint(['message_id'], ['messages.message_id'], name='message_files_ibfk_2'),
    Index('message_id', 'message_id')
)
