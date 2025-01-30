<template>
    <div>
      <h2>Список каталогов</h2>
      <div v-if="childfolders.length === 0">Каталогов для отображения нет</div>
      <ul>
        <li v-for="folder in childfolders" :key="folder.id">
            {{ folder.name }}
            <button @click="selectFolder(folder.id)">Открыть</button>
            <button @click="deleteFolder(folder.id)">Удалить</button>
        </li>
      </ul>
      <div>Текущий каталог: {{ current_folder }}</div>
    </div>
</template>

<script>
    import { mapGetters, mapActions } from 'vuex';

    export default {
      computed: {
        ...mapGetters(["current_folder", "childfolders"]),
      },

      methods: {
        ...mapActions(["fetchContentFolder", "deleteFolder"]),
        
        async selectFolder(folderId) {
          await this.fetchContentFolder(folderId);
          console.log(`Текущий каталог: ${this.current_folder}`)
        },
  }
    };



</script>