<template>
    <div>
      <form @submit.prevent="uploadFile">
        <input type="file" multiple @change="onFilesChange" ref="fileInput" />
        <button type="submit">Загрузить файл</button>
      </form>
    </div>
  </template>


<script>
  import { mapGetters, mapActions } from 'vuex';
  export default {

    data() {
      return {
        selectedFiles: [],
        renamed_files:[],
      };
    },
    computed: {
      ...mapGetters(["current_folder", "files"])
    },
    methods: {
      ...mapActions(["createFile"]),
    //  Обработчик при добавлении файлов в input
      onFilesChange(event) {
        this.selectedFiles = Array.from(event.target.files);
      },
    // Обработчик загрузки файлов на сервер
      async uploadFile() {
        if (!this.selectedFiles) {
            return
        }
        const filenames = this.files.map(obj => obj.description);
        const formData = new FormData();

        this.selectedFiles.forEach((file) => {
            if(filenames.includes(file.name)){
              this.renamed_files.push(file);
              return;
            }
            formData.append("files", file);
            formData.append("folder", this.current_folder)
        });
        await this.createFile(formData);
        this.selectedFiles = [];          
        this.renamed_files.forEach((file) => {
          console.log(`${file.name} уже присутствует в данном каталоге`)
        });
        this.renamed_files = []
        this.$refs.fileInput.value = '';
      },
    },
  };
  </script>
  
  <style>
  /* Добавьте свои стили */
  </style>