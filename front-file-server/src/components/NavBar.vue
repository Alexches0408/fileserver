<template>
    <p>Дерево внизу</p>
    <ul>
      <li v-for="(value, key) in rootElements" :key="key">
        <span @click="toggle">{{value.name}}</span>
        <ul v-if="isOpen&& value.childfolders && value.childfolders.length">
            <TreeNode v-for="(child, index) in value.childfolders" :key="index" :node="child" />
            <li v-for="(value, key) in value.childfiles" :key="key">
                <p>{{ value }}</p>
            </li>
        </ul>
      </li>
    </ul>

</template>

<script>
import { mapState, mapActions } from "vuex"
import TreeNode from "./TreeNode.vue";

export default{
    data() {
    return {
      isOpen: true, // Флаг для раскрытия/свертывания
    };
  },
    components:{
        TreeNode
    },
    computed: {
        ...mapState(["tree"]),
        rootElements() {
            return this.tree
        }
    },
    methods: {
        ...mapActions(["connectWebSocket"]),
        toggle() {
            this.isOpen = !this.isOpen;
        },
    },
    mounted() {
      this.connectWebSocket();
    },
}


</script>


<style>
    .tree {
    list-style-type: none;
    }

    .tree ul {
    margin-left: 20px;
    }

    span {
    cursor: pointer;
    }

</style>