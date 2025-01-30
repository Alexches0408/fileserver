<template>
    <div>
      <h1>Вход</h1>
      <form @submit.prevent="loginuser">
        <input v-model="username" placeholder="Имя пользователя" />
        <input v-model="password" type="password" placeholder="Пароль" />
        <button type="submit">Войти</button>
      </form>
      <p>чтоьы зарегистрироваться нажмите <router-link to="/register">здесь</router-link></p>
    </div>
  </template>
  
  <script>
  import { mapActions } from "vuex";
  
  export default {
    data() {
      return {
        username: "",
        password: "",
      };
    },
    methods: {
      ...mapActions(["login"]),
      async loginuser() {
        const success = await this.login({
          username: this.username,
          password: this.password,
        });
        if (success) {
          this.$router.push("/");
        } else {
          alert("Ошибка входа");
        }
      },
    },
  };
  </script>