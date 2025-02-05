<template>
    <li>
      <span @click="toggle">{{ node.name }}</span>

      <!-- Если у узла есть дети, показываем их только при isOpen === true -->
      <ul v-if="isOpen && node.childfolders && node.childfolders.length">
        <tree-node v-for="(child, index) in node.childfolders" :key="index" :node="child" />
        <li v-for="(value, key) in node.childfiles" :key="key">
            <p>{{ value }}</p>
        </li>
      </ul>
    </li>
</template>

<script>
export default{  
  props: {
    node: Object,
  },
  data() {
    return {
      isOpen: true, // Флаг для раскрытия/свертывания
    };
  },
  template: `

  `,
  methods: {
    toggle() {
      this.isOpen = !this.isOpen;
    },
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