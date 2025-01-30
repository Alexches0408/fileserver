import axios from "axios";
import store from "@/store";

const instance = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

instance.interceptors.request.use(
  async (config) => {
    const accessToken = store.state.token;

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

instance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Если токен истек, обновить его
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshed = await store.dispatch("refreshToken");

      if (refreshed) {
        const newAccessToken = store.state.token;
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return axios(originalRequest);
      } else {
        console.warn('Refresh token истёк, перенаправление на страницу входа.');   
      }
    }

    return Promise.reject(error);
  }
);

export default instance;