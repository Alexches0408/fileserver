<template>
    <div>
      <FullPath/>
      <FileUpload/>
      <FolderCreate/>
      <FileList/>
      <FolderList/>
    </div>
  </template>
  
  <script>
  import { mapActions } from "vuex"
  import FileUpload from "./FileUploadManager.vue"
  import FolderCreate from "./FolderCreateManager.vue"
  import FileList from "./FileListManager.vue"
  import FolderList from "./FolderListManager.vue"
  import FullPath from "./FullPath.vue"

  export default {
    components: {
      FileUpload,
      FolderCreate,
      FileList,
      FolderList,
      FullPath,
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
  </style>