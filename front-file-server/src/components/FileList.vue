<template>
  <HeaderManager/>
  <splitpanes>
    <pane min-size="10" size="20" class="sidebar">
      <FileUpload/>
      <NavBar/> 
    </pane>
    <pane>  
      <div>
        <FullPath/>
        <div id = "file-area" class="min-vh-100" @contextmenu.prevent="showContextMenu($event)">
          <FolderList ref="FolderList"/>
          <FileList/> 
          <ul
            v-if="menuVisible"
            class="dropdown-menu show"
            :style="{ top: `${menuY}px`, left: `${menuX}px`, position: 'absolute' }"
          >
            <li><a class="dropdown-item" href="#" @click="action('Создать папку')">✏️ Создать папку</a></li>
            <li><a class="dropdown-item" href="#" @click="action('Удалить')">🗑️ Удалить</a></li>
            <li><a class="dropdown-item" href="#" @click="action('Поделиться')">📤 Поделиться</a></li>
          </ul>
          <div class="modal fade" ref="modal" tabindex="-1" aria-hidden="true">
              <div class="modal-dialog custom-modal-dialog">
                  <div class="modal-content custom-modal-content">
                      <FolderCreate/>
                  </div>
              </div>
          </div>
        </div>
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
  import HeaderManager from "./HeaderManager.vue"
  import { Modal } from 'bootstrap';

  export default {
    components: {
      FileUpload,
      FolderCreate,
      FileList,
      FolderList,
      FullPath,
      NavBar,
      HeaderManager,
      Splitpanes, 
      Pane,
    },
    data() {
      return {
        menuVisible: false,
        menuX: 0,
        menuY: 0,
        modalInstance: null, 
      };
    },
    methods: {
      ...mapActions(["fetchContentFolder"]),
      showContextMenu(event) {
      // Устанавливаем координаты меню
        this.menuX = event.pageX;
        this.menuY = event.pageY;
        this.menuVisible = true;

        // Закрытие меню при клике в другом месте
        document.addEventListener("click", this.closeContextMenu);
      },
      closeContextMenu() {
        this.menuVisible = false;
        document.removeEventListener("click", this.closeContextMenu);
      },
      action(actionName) {
        if(actionName=="Создать папку") {
          this.$refs.FolderList.createNewFolder();
        }
        this.closeContextMenu();
      },
      openModal() {
        this.modalInstance.show();
      },
      closeModal() {
        this.modalInstance.hide();
      }
    },

    mounted() {
      this.fetchContentFolder();
      this.modalInstance = new Modal(this.$refs.modal);
    },
  };
  </script>
  
  <style>
  /* Добавьте свои стили */
  .sidebar {
    background-color: #f3f4f8;
    color: black;
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
  body {
    margin: 0;
  }

  #file-area{
    display: flex;
    flex-wrap: wrap;
    align-content: flex-start;
  }
  </style>