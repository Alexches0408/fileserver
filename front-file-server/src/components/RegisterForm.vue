<template>
    <div>
      <h1>Регистрация</h1>
      <form @submit.prevent="registeruser">
        <input v-model="username" placeholder="Имя пользователя" />
        <input v-model="password" type="password" placeholder="Пароль" />
        <input v-model="phone" type="phone" placeholder="Номер телефона" />
        <button type="submit">Зарегистрироваться</button>
      </form>
    </div>
  </template>
  
  <script>
  import { mapActions } from "vuex";
  
  export default {
    data() {
      return {
        username: "",
        password: "",
        phone: "",
      };
    },
    methods: {
      ...mapActions(["register"]),
      async registeruser() {
        const success = await this.register({
          username: this.username,
          password: this.password,
          phone_number: this.phone,
        });
        if (success) {
          alert("Регистрация успешна");
          this.$router.push("/login");
        } else {
          alert("Ошибка регистрации");
        }
      },
    },
  };
  </script>