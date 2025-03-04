<template>
    <div id="file-upload">
      <input type="file" multiple @change="onFilesChange" ref="fileInput" style="display: none;"/>
      <div v-for="(file,index) in selectedFiles" class="me-3">
        {{ file.name }}
        <span @click="removeFile(index)" :key="index" class="text-danger"> X</span>
      </div>
      <div v-if="selectedFiles.length===0" @click="triggerInputButton()" class="custom-input">Выбрать файлы</div>
      <div v-if="selectedFiles.length>0" @click="uploadFile()" class="custom-input">Загрузить файл</div>
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
      triggerInputButton(){
        this.$refs.fileInput.click();
      },
      removeFile(index){
        this.selectedFiles.splice(index,1)
      }
    },
  };
  </script>
  
  <style>
  #file-upload{
    width: 90%;
    min-height: 80px;
    justify-self: center;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    padding: 16px;
    border-radius: 5px;
    border: solid 1px #c9cacd;
    background-color: #fff;
  }

  .custom-input {
    width: 129px;
    height: 48px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 4px;
    padding: 8px 10px;
    border-radius: 5px;
    background-color: #f8d447;
    margin-left: auto;
  }
  </style>