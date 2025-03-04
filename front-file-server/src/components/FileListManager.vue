<template>
    <div v-if="files.length === 0">Нет файлов для отображения.</div>
    <div v-for="file in files" :key="file.id" @contextmenu.stop.prevent="openContextmenu($event, file.id)" class="file">
      <img :src="file.thumbnail ? file.thumbnail : `/icons/${file.icon}`" alt="" srcset="">
      <span>{{ file.description }}</span>
    </div>
    <ContextMenu ref="contextMenu"/>
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
      ...mapActions(["deleteFile"]),
      openContextmenu(event, fileId){
        this.$refs.contextMenu.showContext(event, fileId)
      },

      }
}

</script>


<style>
.file {
  width: 135px;
  height: 166px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 4px;
  padding: 12px;
}
</style>
