import axios from 'axios'
import Cookies from "js-cookie";

var csrftoken = Cookies.get("csrftoken");
axios.defaults.headers.common["X-CSRFToken"] = csrftoken;
axios.defaults.headers.common["Content-Type"] = "application/json";
export default axios.create({
    baseURL: "http://127.0.0.1:8000/",

});