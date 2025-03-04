<template>
    <div v-if="visible" 
    class="context-menu"
    :style="{top: `${position.y}px`, left: `${position.x}px`}">
        <ul>
            <li @click="handleAction('удалить')">Удалить элемент</li>
            <li @click="handleAction('копировать')">Копировать элемент</li>
        </ul>

    </div>

</template>

<script>
import { mapActions } from 'vuex';
export default {
    data () {
        return {
            visible: false,
            position: {x:0, y:0},
            folderId:"",
            elemType:"",
        };
    },
    methods: {
        ...mapActions(["deleteFolder"]),
        showContext(event, folderId) {
            event.preventDefault();
            this.position= {x: event.clientX, y: event.clientY};
            this.folderId = folderId;
            this.visible=true;
         },
         hideMenu() {
            this.visible = false;
         },
         handleAction(action) {
            if (action=="удалить") {
                console.log(this.folderId)
                this.deleteFolder(this.folderId);
                this.folderId = "";               
            }
            this.hideMenu();
         },
    },
    mounted(){
        document.addEventListener('click', this.hideMenu);
    },
    beforeUnmount(){
        document.removeEventListener('click', this.hideMenu);
    }
}

</script>

<style>
.context-menu {
  position: absolute;
  background: white;
  border: 1px solid #ccc;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}
.context-menu ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
.context-menu li {
  padding: 8px 16px;
  cursor: pointer;
}
.context-menu li:hover {
  background: #f0f0f0;
}
</style>