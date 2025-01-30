<template>
    <div>
        <div>
            <span @click="reset()" style="cursor: pointer;">Главная</span>
            
            <span v-for="(segment, index) in FullPath" :key="index">
                <span> / </span>
                <span @click="navigateTo(index)" style="cursor: pointer;">
                    {{ segment }}
                </span>
            </span>
        </div>

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