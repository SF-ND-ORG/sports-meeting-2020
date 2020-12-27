<template>
  <div class="class">
    <v-row>
      <v-col>
        <v-select
          :items="grade_items"
          item-text="text"
          item-value="value"
          v-model="grade_selection"
          label="年级"
          flat
        ></v-select
      ></v-col>
      <v-col>
        <v-select
          :items="class_items"
          item-text="text"
          item-value="value"
          label="班级"
          v-model="class_selection"
          flat
        ></v-select
      ></v-col>
      <v-col
        class="mt-3"
        width="10px"
        style="max-width: 170px"
        v-show="wl_show"
      >
        <v-btn-toggle v-model="toggle_wl" dense mandatory>
          <v-btn>
            <div>文</div>
          </v-btn>

          <v-btn>
            <div>理</div>
          </v-btn>
        </v-btn-toggle>
      </v-col>
    </v-row>
    <v-btn color="info" style="" @click="onquery">查询</v-btn>
  </div>
</template>

<script>
export default {
  data: () => ({
    grade_selection: 23,
    class_selection:0,
    grade_items: [
      { text: "高一", value: 23 },
      { text: "高二", value: 22 },
      { text: "高三", value: 21 },
    ],
    wl_show: false,
    toggle_wl: 0,
  }),

  watch: {
    grade_selection: function () {
      if (this.grade_selection < 23) {
        this.wl_show = true;
      } else {
        this.wl_show = false;
      }
    },
  },

  methods: {
    onquery() {
      var wl = "";
      if (this.toggle_wl == 0) {
        wl = "W";
      } else if (this.toggle_wl == 1) {
        wl = "L";
      }
      if (this.grade_selection == 23) {
        wl = "";
      }
      let api =
        "http://114.55.93.225:5706/getgrades/byclass/?grades=" +
        this.grade_selection +
        "&class=" +
        wl +
        this.class_selection 
      this.axios.get(api).then((response) => {
        this.$emit("onquery", response.data.data);
      });
    },
  },

  computed: {
    class_items: function () {
      let res = [];
      switch (this.grade_selection) {
        case 1: {
          for (var i = 1; i <= 18; i++) {
            res.push({ text: i.toString() + "班", value: i });
          }
          break;
        }
        default: {
          for (var ii = 1; ii <= 18; ii++) {
            res.push({ text: ii.toString() + "班", value: ii });
          }
        }
      }
      return res;
    },
  },
};
</script>

<style>
</style>