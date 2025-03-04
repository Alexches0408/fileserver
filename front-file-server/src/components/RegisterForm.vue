<template>
  <div id="register-page">
    <div id="register-form">
      <div>
        <span>иконка</span>
        <br>
        <span>ФЛОБ</span>
      </div>
      <router-link to="/login" id="login-link" class="d-flex justify-content-start w-100"><span><img src="/icons/arrow-left.svg" alt=""></span>Назад</router-link>
      <div id="register-input">
        <label for="username">Логин</label>
        <input v-model="username" placeholder="Имя пользователя" id="username" class="mb-2"/>
        <label for="password">Пароль</label>
        <input v-model="password" type="password" placeholder="Пароль" id="password" class="mb-2"/>
        <label for="password2">Повторите пароль</label>
        <input v-model="password2" type="password" placeholder="Повторите пароль" id="password2" @keyup.enter="registeruser()"/>
      </div>
      <div @click="registeruser()" id="register-button">Зарегистрироваться</div>
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
        password2: "",
      };
    },
    methods: {
      ...mapActions(["register"]),
      async registeruser() {
        if (this.password !== this.password2) {
          alert('Пароли не совпадают');
          return;
        }
        const success = await this.register({
          username: this.username,
          password: this.password,
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

  
<style scoped>
#register-page{
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 15vh;
  width: 100%;
  height: 100%;
}

#register-form{
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

#login-link {
  text-decoration: none;
  font-family: Roboto;
  font-size: 22px;
  line-height: 1.27;
  letter-spacing: normal;
  color: #000;
}

#register-input {
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


#register-button{
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
</style>