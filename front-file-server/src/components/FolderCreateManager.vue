<template>
    <form @submit.prevent="createNewFolder">
        <input v-model="newFolder" placeholder="Название каталога"/>
        <button type="submit">Создать каталог</button>
    </form>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

    export default {
        data() {
        return {
            newFolder:"",
        };
        },
        computed: {
            ...mapGetters(["current_folder", "childfolders"])
        },
        methods: {
            ...mapActions(["createFolder"]),
            createNewFolder() {
                const folderNames = this.childfolders.map(obj => obj.name);
                if (folderNames.includes(this.newFolder)){
                    console.log("Такой каталог уже есть")   
                    return;
                }
                const data = {
                    name: this.newFolder,
                    parent_folder: this.current_folder ? this.current_folder : null,
                };
                this.createFolder(data);
                this.newFolder="";
            }
 
            }

        }

  </script>
  
  <style>
  /* Добавьте свои стили */
  </style>