<template>
  <splitpanes>
    <pane min-size="10" size="20" class="sidebar">
      <NavBar/> 
    </pane>
    <pane>  
      <div>
        <FullPath/>
        <FileUpload/>
        <FolderCreate/>
        <FileList/>
        <FolderList/>
      </div>
    </pane>
  </splitpanes>
</template>
  
  <script>
  import { mapActions } from "vuex"
  import FileUpload from "./FileUploadManager.vue"
  import FolderCreate from "./FolderCreateManager.vue"
  import FileList from "./FileListManager.vue"
  import FolderList from "./FolderListManager.vue"
  import FullPath from "./FullPath.vue"
  import { Splitpanes, Pane } from 'splitpanes'
  import 'splitpanes/dist/splitpanes.css'
  import NavBar from "./NavBar.vue"

  export default {
    components: {
      FileUpload,
      FolderCreate,
      FileList,
      FolderList,
      FullPath,
      NavBar,
      Splitpanes, 
      Pane,
    },
    methods: {
      ...mapActions(["fetchContentFolder"]),
    },

    mounted() {
      this.fetchContentFolder();
    },
  };
  </script>
  
  <style>
  /* Добавьте свои стили */
  .sidebar {
    background: #333;
    color: white;
    padding: 10px;
    height: 100vh;
  }
  .content {
    padding: 20px;
  }
  .splitpanes__splitter {
  width: 6px; /* Ширина разделителя */
  cursor: ew-resize; /* Курсор изменения размера */
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.2); /* Добавление тени */
}
  </style>