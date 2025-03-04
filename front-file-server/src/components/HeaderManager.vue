<template>
    <header>
        <div id="logo">
            <div id="logo-text">ЛИМС</div>
        </div>
        <div id="search">Здесь будет поиск</div>
        <div id="user-pop-up" @click="openModal">Личная инфа</div>
        <div class="modal fade" ref="modal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog custom-modal-dialog">
                <div class="modal-content custom-modal-content">
                    <div class="modal-body">
                        <div id="avatar">Аватар</div>
                        <div>Сменить пароль(пока нет)</div>
                        <div @click.prevent=logoutUser()>
                            <span>иконка</span>
                            <span>Выйти</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header>    
</template>

<script>
import { Modal } from 'bootstrap';
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      modalInstance: null, // Экземпляр Bootstrap Modal
    };
  },
  mounted() {
    this.modalInstance = new Modal(this.$refs.modal);
  },
  methods: {
    ...mapActions(["logout"]),
    logoutUser(){
        this.closeModal()
        this.logout();
        this.$router.replace("/login")
    },
    openModal() {
      this.modalInstance.show();
    },
    closeModal() {
      this.modalInstance.hide();
    }
  }
};

</script>

<style scoped>
header {
    height: 71px;
    padding: 0 40px 0 0;
    background-color: #a7a8ab;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

#logo {
    background-color: #f8d447;
    width: 165px;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

#logo-text{
    font-size: 32px;
}

#search {
  width: 680px;
  height: 44px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  border-radius: 5px;
  border: solid 1px #c9cacd;
  background-color: #fff;
}

#user-pop-up {
  width: 170px;
  height: 48px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
  border-radius: 5px;
  background-color: #fff;
}

/* .custom-modal-dialog{
  top: 100px;
  left: 50%;
} */

.custom-modal-content{
    width: 324px;
    height: 286px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 12px;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 1px 1px 6px 0 rgba(0, 0, 0, 0.25);
    border: solid 1px #c9cacd;
    background-color: #f3f4f8;
}

#avatar{
    width: 179px;
    height: 158px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 12px;
    padding: 20px;
    border-radius: 5px;
    background-color: #fff;
}

</style>