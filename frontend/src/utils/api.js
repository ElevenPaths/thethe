let baseURL = "https://localhost";
if (process.env.NODE_ENV === "development") {
  baseURL = "https://localhost:8000";
}

const axios = require("axios").create({ baseURL: baseURL });

import { AUTH_LOGOUT } from "../store/actions/auth";
import router from "../router";
import store from "../store";

// This snippet is for global-cached axios header for token
/* const token = localStorage.getItem("user-token");
if (token) {
  axios.defaults.headers.common.Authorization = token;
} */

axios.interceptors.response.use(
  function(response) {
    return response;
  },
  function(error) {
    console.log("Axios error:" + error);
    if (error.response && error.response.status === 401) {
      store.dispatch(AUTH_LOGOUT);
      router.push("/login");
    }
    return Promise.reject(error);
  }
);

const api_call = ({ url, ...args }) => {
  const token = localStorage.getItem("user-token");
  const headers = {};
  if (token) {
    headers.Authorization = token;
  }
  return axios.post(url, args, { headers: headers });
};

export default api_call;
