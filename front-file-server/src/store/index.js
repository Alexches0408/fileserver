import { createStore } from 'vuex';
import axiosInstance from '../axios'
import axios from 'axios';

const store = createStore({
    state () {
        return {
            current_folder: null,
            childfolders: [],
            files:[],
            FullPath:{},
            token: localStorage.getItem("accessToken") || null,
            refreshToken: localStorage.getItem("refreshToken") || null,
            user: null,
            tree: null,
        };
    },
    mutations: {
        SET_CURRENT_FOLDER(state, folder) {
            state.current_folder = folder;
        },
        SET_FOLDERS(state, childfolders) {
            state.childfolders = childfolders;
        },
        SET_FILES(state, files) {
            state.files = files;
        },
        SET_FULL_PATH(state, FullPath){
            state.FullPath = FullPath;
        },
        SET_TOKEN(state, token) {
            state.token = token;
            localStorage.setItem("accessToken", token);
        },
        SET_REFRESH_TOKEN(state, refreshToken) {
            state.refreshToken = refreshToken;
            localStorage.setItem("refreshToken", refreshToken);
        },
        CLEAR_TOKENS(state) {
            state.token = null;
            state.refreshToken = null;
            localStorage.removeItem("accessToken");
            localStorage.removeItem("refreshToken");
        },
        SET_USER(state, user) {
            state.user = user;
        },
        SET_TREE(state, payload) {
            state.tree = payload;
          },
    },
    actions: {
        async fetchFiles({commit}) {
            try {
                const response = await axiosInstance.get(`http://127.0.0.1:8000/files/files/?folder_is_empty=true`)
                commit("SET_FILES", response.data)
            } catch (error) {
                console.error(`Ошибка при получении файлов директории`)
            }
        },
        async fetchFolders({commit}) {
            try {
                const response = await axiosInstance.get(`http://127.0.0.1:8000/files/folders/?parent_folder_is_empty=true`)
                commit("SET_FOLDERS", response.data)
            } catch (error) {
                console.error("Ошибка при получении дочерних каталогов", error);
            }           
        },
        async fetchFullPath({commit}, folderId) {
            const response = await axiosInstance.get(`http://127.0.0.1:8000/files/folders/${folderId}/`);
            commit("SET_FULL_PATH", response.data.full_path);
        },        
        async fetchContentFolder({commit, dispatch}, folderId) {
            const url = folderId
            ? `http://127.0.0.1:8000/files/folders/${folderId}/content_folder/`
            : `http://127.0.0.1:8000/files/folders/`
            const response = await axiosInstance.get(url)
            if (folderId) { 
                const folder = response.data;
                commit("SET_CURRENT_FOLDER",folderId);
                commit("SET_FOLDERS", folder.childfolders);
                commit("SET_FILES", folder.files);
                dispatch("fetchFullPath", folderId)
            }
            else{
                dispatch("fetchFiles");
                commit("SET_CURRENT_FOLDER",null);
                dispatch("fetchFolders");
                commit("SET_FULL_PATH", {})
            }},
        async createFolder({ dispatch, state }, data) {
            try {
                await axiosInstance.post(`http://127.0.0.1:8000/files/folders/`, data);
                await dispatch("fetchContentFolder", state.current_folder);
            } catch (error) {
                console.log(`Ошибка при создании каталога ${error}`)
            }
        },

        async deleteFolder({ dispatch, state }, folderId) {
            if(!confirm("Вы уверены что хотите удалить выбранный каталог")){return;}
            try {
                await axiosInstance.delete(`http://127.0.0.1:8000/files/folders/${folderId}/`);
                await dispatch("fetchContentFolder", state.current_folder);
            } catch (error) {
                console.log(`Ошибка при удалении каталога ${error}`)
            }
        },
        async createFile({ dispatch, state }, data) {
            try {
                await axiosInstance.post(`http://127.0.0.1:8000/files/files/`, data);
                await dispatch("fetchContentFolder", state.current_folder);
            } catch (error) {
                console.log(`Ошибка при создании файла ${error}`)
            }
        },
        async deleteFile({ dispatch, state }, fileId) {
            if(!confirm("Вы уверены что хотите удалить выбранный файл")){return;}
            try{
                await axiosInstance.delete(`http://127.0.0.1:8000/files/files/${fileId}/`);
                await dispatch("fetchContentFolder", state.current_folder);
            } catch (error) {
                console.log(`Ошибка при удалении файла ${error}`)
            }
        },
        async login({ commit }, credentials) {
            try {
                const response = await axios.post("http://127.0.0.1:8000/api/auth/token/", credentials);
                commit("SET_TOKEN", response.data.access);
                commit("SET_REFRESH_TOKEN", response.data.refresh);
                return true;
            } catch (error) {
                console.error("Ошибка входа", error);
                return false;
            }
                        
        },
        async refreshToken({ state, commit }) {
            try {
                const response = await axios.post("http://127.0.0.1:8000/api/auth/token/refresh/", {
                refresh: state.refreshToken
            });
            commit("SET_TOKEN", response.data.access);
            return true;
            } catch (error){
                commit("CLEAR_TOKENS");
                return false;
            }
        },
        async register(_, userdata) {
            try {
                await axios.post("http://127.0.0.1:8000/api/auth/register/", userdata);
                return true;
            } catch(error){
                console.error("Ошибка регистрации пользователя", error);
                return false;
            }
        },
        async logout({ commit }) {
            commit("CLEAR_TOKENS");
            commit("SET_USER", null);
        },
        connectWebSocket({ commit }) {
            const socket = new WebSocket("ws://127.0.0.1:8000/ws/json-updates/");
            socket.onmessage = (event) => {
            const newData = JSON.parse(event.data);
            commit("SET_TREE", newData); // Обновляем хранилище
            };
            
    
            socket.onerror = (error) => {
            console.error("Ошибка WebSocket:", error);
            };
        },
         
    }, 
    getters: {
        current_folder: (state) => state.current_folder,
        childfolders: (state) => state.childfolders,
        files: (state) => state.files,
        FullPath: (state) => state.FullPath,
        isAuthenticated: (state) => !!state.token,
      },

})

export default store;