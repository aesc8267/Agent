import axios from 'axios'
function hello_world() {
    return axios.get('api').catch(error => {
        console.log(error);
    })
}
export { hello_world }