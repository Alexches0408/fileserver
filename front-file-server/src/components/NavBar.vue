<template>
    <div id="allfiles">Все файлы</div>
    <div class="no-bullets">
      <div v-for="(value, key) in rootElements" :key="key">
        <div v-if="key!=='files' && (Object.keys(value.childfiles).length > 0 || Object.keys(value.childfolders).length > 0)" @click="oneClick(value.id)" class="headroot">
            <span v-if="Object.keys(value.childfiles).length > 0 || Object.keys(value.childfolders).length > 0" class="arrowexist"><img src="/icons/arrow-right.svg" :id="'arrowicon'+value.id"></span>
            <span><img src="/icons/folder-close.svg" :id="'foldericon'+value.id"></span>
            <span>{{value.name}}</span>
        </div>
        <div v-if="key!=='files' && (Object.keys(value.childfiles).length > 0 || Object.keys(value.childfolders).length > 0)" :id="'folder'+value.id" style="display: none;" class="childlist">
            <div class="childitemcontent">
                <TreeNode v-for="(child, index) in value.childfolders" :key="index" :node="child" />
                <div v-for="(val, key) in value.childfiles" :key="key" class="childfile">
                    <div @click="selectFolder(value.id)" class="filename">
                        <img :src="getFileIcon(val)" alt="icon">
                        {{ val }}
                    </div>
                </div>
            </div>
        </div>
    </div>
      <div v-for="(value, key) in rootElements" :key="key">
        <div v-if="key!=='files' && (Object.keys(value.childfiles).length == 0 && Object.keys(value.childfolders).length == 0)" @click="selectFolder(value.id)" class="headrootempty">
            <span v-if="Object.keys(value.childfiles).length > 0 || Object.keys(value.childfolders).length > 0" class="arrowexist"><img src="/icons/arrow-right.svg" :id="'arrowicon'+value.id"></span>
            <span><img src="/icons/folder-close.svg" :id="'foldericon'+value.id"></span>
            <span>{{value.name}}</span>
        </div>
      </div>
      <div v-for="(file, key) in rootFiles" :key="key">
        <div class="headrootempty" @click="selectFolder()">
            <span><img :src="getFileIcon(file)" alt="icon"></span>
            {{ file }}
        </div>
      </div>
    </div>
</template>

<script>
import { mapState, mapActions } from "vuex"
import TreeNode from "./TreeNode.vue";

export default{
    data() {
    return {
      isOpen: true, // Флаг для раскрытия/свертывания
      delay: 300,
      clicks: 0,
      timer: null,
    };
  },
    components:{
        TreeNode
    },
    computed: {
        ...mapState(["tree"]),
        rootElements() { 
            if (this.tree) {
                const filtered = {}
                for (const[key, value] of Object.entries(this.tree)){
                    if (key!=='files'){
                        filtered[key]=value;
                    }
                }
                return filtered
            }
            return this.tree;
        },
        rootFiles(){
            if (this.tree) {
                const files = this.tree['files']
                return files
            }
            return;
        }
    },
    methods: {
        ...mapActions(["connectWebSocket", "fetchContentFolder", "selectFolder"]),
        toggle(folderId) {
            let elem = document.getElementById("folder"+folderId)
            if (elem.style.display==="none") {
                elem.style.display="block"
                let arrowicon = document.getElementById("arrowicon"+folderId)
                let foldericon = document.getElementById("foldericon"+folderId)
                arrowicon.src = "/icons/arrow-bottom.svg"
                foldericon.src = "/icons/folder-open.svg"
            } else {
                elem.style.display="none"
                let arrowicon = document.getElementById("arrowicon"+folderId)
                let foldericon = document.getElementById("foldericon"+folderId)
                arrowicon.src = "/icons/arrow-right.svg"
                foldericon.src = "/icons/folder-close.svg"
            }
        },
        async selectFolder(folderId) {
            await this.fetchContentFolder(folderId);
        },
        oneClick(folderId) {
            this.clicks++;
            if (this.clicks === 1) {
            this.timer = setTimeout( () => {
                this.toggle(folderId)
                this.clicks = 0
            }, this.delay);
            } else {
                clearTimeout(this.timer);  
                this.selectFolder(folderId)
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
    mounted() {
      this.connectWebSocket();

    }, 
}


</script>


<style scoped>
    #allfiles { 
        display: flex;
        justify-self: start;
    }
    .headroot {
        display: flex;
        align-items: center;
    }
    .headrootempty {
        display: flex;
        align-items: center;
        padding-left: 25px;
    }
    .childlist{
        padding: 0;
    }
    .childfile {
        display: flex;
        margin-left: 25px;
    }
    .childitemcontent {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-left: 20px;
    }
    .filename{
        display: flex;
        align-items: center;
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
        padding: 0;
    }
    .child {
        display: none;
    }


</style>