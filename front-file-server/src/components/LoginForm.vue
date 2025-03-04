<template>
  <div id="login-page">
    <div id="login-form">
      <div>
        <span>иконка</span>
        <br>
        <span>ФЛОБ</span>
      </div>
      <div id="login-input">
        <label for="username">Логин</label>
        <input v-model="username" placeholder="Имя пользователя" id="username" class="mb-3"/>
        <label for="password">Пароль</label>
        <input v-model="password" type="password" placeholder="Пароль" id="password" @keyup.enter="loginuser()"/>
        <div id="repair-pass">Добавить восстановление пароля</div>
      </div>
      <div>
        <div @click="loginuser()" id="login-button" class="mb-3">Войти</div>
        <router-link to="/register" id="register-link">Регистрация</router-link>
      </div>
    </div>
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

<style scoped>
#login-page{
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 15vh;
  width: 100%;
  height: 100%;
}

#login-form{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  width: 25vw;
  height: 65vh;
  padding: 77px 98px 58px;
  border-radius: 14px;
  border: solid 1px #a7a8ab;
  background-color: #f3f4f8;
}

#login-input {
  display: flex;
  flex-direction: column;
}

label {
  font-family: Roboto;
  font-size: 14px;
  font-weight: 500;
  font-stretch: normal;
  font-style: normal;
  line-height: 1.43;
  letter-spacing: 0.1px;
  text-align: left;
  color: #636365;
}

input {
  width: 100%;
  height: 38px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  border-radius: 5px;
  border: solid 1px #c9cacd;
  background-color: #fff;
  font-family: Roboto;
  font-size: 16px;
  line-height: 1.5;
  letter-spacing: 0.5px;
}

#repair-pass{
  font-family: Roboto;
  font-size: 12px;
  line-height: 1.5;
  letter-spacing: 0.5px;
  text-align: left;
  color: #636365;
}

#login-button{
  width: 200px;
  height: 48px;
  display: flex;
  justify-content: center;
  align-items: center;
  justify-self: center;
  gap: 10px;
  border-radius: 5px;
  background-color: #f8d447;
  font-family: Roboto;
  font-size: 16px;
  line-height: 1.5;
  letter-spacing: 0.5px;
}

#register-link{
  text-decoration: none;
  font-family: Roboto;
  font-size: 16px;
  line-height: 1.5;
  letter-spacing: 0.5px;
  color: #636365;
}

</style>