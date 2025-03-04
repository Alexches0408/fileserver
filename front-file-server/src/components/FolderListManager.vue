<template>
    <div v-if="childfolders.length === 0">Каталогов для отображения нет</div>
    <div v-for="folder in childfolders" :key="folder.id" class="folder" @contextmenu.stop.prevent="openContextmenu($event, folder.id)" @dblclick="selectFolder(folder.id)">
        <img src="/icons/folder.svg" alt="" srcset="">
        {{ folder.name }}
        <!-- <button @click="selectFolder(folder.id)">Открыть</button>
        <button @click="deleteFolder(folder.id)">Удалить</button> -->
    </div>
    <FolderContextMenu ref="contextMenu"/>
</template>

<script>
    import { mapGetters, mapActions } from 'vuex';
    import FolderContextMenu from './FolderContextMenu.vue';

    export default {
      data() {
        return {
            baseNameFolder:"Новая папка",
            i: 2,
        };
      },
      components: {
        FolderContextMenu
      },
      computed: {
        ...mapGetters(["current_folder", "childfolders"]),
        folderName() {
          return `${this.baseNameFolder} ${this.i}`
        },
      },

      methods: {
        ...mapActions(["fetchContentFolder", "deleteFolder", "createFolder"]),
        
        async selectFolder(folderId) {
          await this.fetchContentFolder(folderId);
        },

        createNewFolder(){
          console.log("Пошла мазута")
          const folderNames = this.childfolders.map(obj => obj.name);
          if (folderNames.includes(this.baseNameFolder)){
            while (folderNames.includes(this.folderName)) {
              this.i+=1;
            };
            this.baseNameFolder = this.folderName;
          }
          const data = {
                    name: this.baseNameFolder,
                    parent_folder: this.current_folder ? this.current_folder : null,
                };
          this.createFolder(data);
          this.i = 2;
          this.baseNameFolder="Новая папка"
        },
        openContextmenu(event, folderId){
          this.$refs.contextMenu.showContext(event, folderId);
        },
      }
    };



</script>

<style>
.folder-list{
  display: flex;
}

.folder {
  width: 135px;
  height: 166px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 4px;
  padding: 12px;
  border-radius: 5px;
}

</style>