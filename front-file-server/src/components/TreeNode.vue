<template>
    <div class="root">
        <div v-if="key!=='files' && (Object.keys(node.childfiles).length > 0 || Object.keys(node.childfolders).length > 0)" @click="oneClick(node.id)" class="nodeheader">
            <span><img src="/icons/arrow-right.svg" :id="'arrowicon'+node.id"></span>
            <span><img src="/icons/folder-close.svg" :id="'foldericon'+node.id"></span>
            {{node.name}}
        </div>
        <div v-if="key!=='files'&& (Object.keys(node.childfiles).length == 0 && Object.keys(node.childfolders).length == 0)" @click="selectFolder(node.id)" class="nodeheaderempty">
            <span><img src="/icons/folder-close.svg" :id="'foldericon'+node.id"></span>
            {{node.name}}
        </div>
      <!-- Если у узла есть дети, показываем их только при isOpen === true -->
        <div v-if="isOpen" class="no-bullets node">
            <tree-node v-for="(child, index) in node.childfolders" :key="index" :node="child" />
            <div v-for="(value, key) in node.childfiles" :key="key" class="nodefiles">
                <div @click="selectFolder(node.id)" class="nodefileselem">
                  <span><img :src="getFileIcon(value)" alt="icon"></span>
                  {{ value }}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
export default{  
  props: {
    node: Object,
  },
  data() {
    return {
      isOpen: false, // Флаг для раскрытия/свертывания
      delay: 300,
      clicks: 0,
      timer: null
    };
  },
  methods: {
    ...mapActions(["fetchContentFolder"]),
    toggle(nodeId) {
        this.isOpen = !this.isOpen;
        if (this.isOpen) {
                let arrowicon = document.getElementById("arrowicon"+nodeId)
                let foldericon = document.getElementById("foldericon"+nodeId)
                arrowicon.src = "/icons/arrow-bottom.svg"
                foldericon.src = "/icons/folder-open.svg"
            } else {
                let arrowicon = document.getElementById("arrowicon"+nodeId)
                let foldericon = document.getElementById("foldericon"+nodeId)
                arrowicon.src = "/icons/arrow-right.svg"
                foldericon.src = "/icons/folder-close.svg"
            }
    },
    async selectFolder(folderId) {
        await this.fetchContentFolder(folderId);
    },
    oneClick(nodeId) {
          this.clicks++;
          if (this.clicks === 1) {
            this.timer = setTimeout( () => {
                this.toggle(nodeId)
                this.clicks = 0
            }, this.delay);
          } else {
             clearTimeout(this.timer);  
             this.selectFolder(nodeId)
             this.clicks = 0;
          }         
      },
      getFileIcon(filename){
            const extension = filename.split(".").pop().toLowerCase();
            const icons = {
                svg: "/icons/image.svg",
                jpg: "/icons/image.svg",
                jpeg: "/icons/image.svg",

            };
            return icons[extension] || "/icons/default.svg"
        }     

  },
}
</script>

<style>
.root {
    display: flex;
    flex-direction: column;
}
.tree {
  list-style-type: none;
}

.tree ul {
  margin-left: 20px;
}

span {
  cursor: pointer;
}

.no-bullets {
    list-style-type: none; /* Убирает маркеры */
}

.nodeheader{
    display: flex;
    align-items: center;
}

.nodeheaderempty { 
    display: flex;
    align-items: center;
    margin-left: 25px;
}

.node {
    display: flex;
    flex-direction: column;
    margin-left:25px;
}

.nodefiles{
    display: flex;
    margin-left: 25px;

} 

.nodefileselem {
    display: flex;
    align-items: center;
}
</style>