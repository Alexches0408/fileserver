<template>
  <div>
    <div>
      <p>{{  isAuthenticated }}</p>
      <p>чтоьы зарегистрироваться нажмите <router-link to="/register">здесь</router-link></p>
      <p>чтоьы залогиниться нажмите <router-link to="/login">здесь</router-link></p>
      <p>чтоьы разлогиниться нажмите <span @click.prevent=logoutUser()>здесь</span></p>
      <h1>Список файлов</h1>
        <div v-if="files.length === 0">Нет файлов для отображения.</div>
        <ul>
          <li v-for="file in files" :key="file.id" @contextmenu.prevent="openContextmenu($event, file.id)">
            <a :href="file.folder ? `http://127.0.0.1:8000${file.file}` : `${file.file}` " target="_blank">{{ file.description }}</a>
            <button @click="deleteFile(file.id)">Удалить</button>
          </li>
        </ul>
    </div>
    <ContextMenu ref="contextMenu"/>
  </div>
</template>

<script>
import ContextMenu from "./ContextMenu.vue";
import { mapGetters, mapActions } from 'vuex';
export default{
    components: {
      ContextMenu
    },
  
    computed: {
      ...mapGetters(["files", "current_folder", "isAuthenticated"]),
    },
    
    methods:{
      ...mapActions(["deleteFile", "logout"]),
      openContextmenu(event, fileId){
        this.$refs.contextMenu.showContext(event, fileId)
      },
      logoutUser(){
        this.logout();
        this.$router.replace("/login")
      },

      }
}




</script>