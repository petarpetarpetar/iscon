import axios from 'axios'

const axiosClient = axios.create({
    baseURL: 'https://www.themealdb.com/api/json/v1/1/', //todo: base url
    // timeout: 1000,
    // headers: {'X-handler' : 'foobar'}  //Check out documentation
});

export default axiosClient;