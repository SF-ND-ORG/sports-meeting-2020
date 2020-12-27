<template>
  <v-container
    ><v-card class="ma-2">
      <v-card-title primary-title> 成绩查询 </v-card-title>
      <v-card-text>
        <v-btn-toggle v-model="toggle_exclusive" dense mandatory>
          <v-btn>
            <div>按班级</div>
          </v-btn>

          <v-btn>
            <div>按姓名</div>
          </v-btn>

          <v-btn>
            <div>按项目</div>
          </v-btn>
        </v-btn-toggle>
      </v-card-text>
    </v-card>
    <v-card class="ma-2" id="query">
      <v-card-text>
        <querybyclass
          v-show="toggle_exclusive == 0"
          @onquery="onquery"
        ></querybyclass>
        <querybyname
          v-show="toggle_exclusive == 1"
          @onquery="onquery"
        ></querybyname>
        <querybyproject v-show="toggle_exclusive == 2" @onquery="onquery">
        </querybyproject>
      </v-card-text>
    </v-card>
    <v-card class="ma-2" id="display">
      <v-card-text
        v-show="display_array !== undefined && display_array.length > 0"
      >
        <v-data-table :headers="headers" :items="display_array"></v-data-table>
      </v-card-text>
      <v-card-text v-show="display_array.length == 0 && flag == true">
        <v-alert dense outlined type="error">
          未找到对应结果，请更改查询条件后重试
        </v-alert>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import querybyclass from "./query_compoments/querybyclass";
import querybyname from "./query_compoments/querybyname.vue";
import Querybyproject from "./query_compoments/querybyproject.vue";

export default {
  components: { querybyclass, querybyname, Querybyproject },
  data: () => ({
    display_array: [],
    flag: false,
    headers: [
      { text: "届数", value: "grades" },
      { text: "班级", value: "class" },
      { text: "姓名", value: "name" },
      { text: "项目", value: "projects" },
      { text: "成绩", value: "achievements" },
      { text: "此项目排名", value: "rank" },
    ],
    toggle_exclusive: 0,
    grade_items: ["高一", "高二", "高三"],
  }),
  methods: {
    onquery(data) {
      this.display_array = data;
      this.flag=true
    },
  },
};
</script>

<style>
</style>