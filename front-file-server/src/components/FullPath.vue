<template>
    <div id="full-path">
        <span @click="reset()" style="cursor: pointer;">Главная</span>
        <span v-for="(segment, index) in FullPath" :key="index">
            <span> > </span>
            <span @click="navigateTo(index)" style="cursor: pointer;">
                {{ segment }}
            </span>
        </span>
    </div>
</template>


<script>
import { mapGetters, mapActions } from 'vuex';

export default {
    computed: {
        ...mapGetters(["FullPath"]),
    },
    methods: {
        ...mapActions(["fetchContentFolder"]),

        navigateTo(folder_id){
            this.fetchContentFolder(folder_id);
        },
        reset(){
            this.fetchContentFolder();
        },
    },
}

</script>

<style>
#full-path {
    padding-left: 20px;
    padding-top: 20px;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    font-size: 14px;
    font-weight: 500;
    font-stretch: normal;
    font-style: normal;
    line-height: 1.43;
    letter-spacing: 0.1px;
    color: #636365;
}
</style>