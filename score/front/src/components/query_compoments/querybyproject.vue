<template>
  <div class="class">
    <v-select
      :items="items"
      v-model="project_selection"
      label="项目名称"
    ></v-select>
    <v-btn color="info" style="" @click="onquery">查询</v-btn>
  </div>
</template>

<script>
import AppVue from "../../App.vue";
export default {
  data: () => ({
    project_selection: "",
    items: [],
  }),

  methods: {
    onquery() {
      let api = "http://114.55.93.225:5706/getgrades/bypro/?projects="+this.project_selection;
      this.axios.get(api).then((response) => {
        this.$emit("onquery",response.data.data)
      });
    },
  },

  mounted: function () {
    console.log("mounted");
    let api = "http://114.55.93.225:5706/projects";
    this.axios.get(api).then((response) => {
      console.log(response.data);
      this.items = response.data.data;
    });
  },
};
</script>

<style>
</style>