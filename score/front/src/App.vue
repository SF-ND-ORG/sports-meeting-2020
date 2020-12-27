<template>
  <v-app id="inspire">
    <v-navigation-drawer v-model="drawer" app clipped>
      <v-list dense>
        <!-- v-subheader 是组的标题 -->
        <v-list>
          <v-list-item-group>
            <v-list-item v-for="(item, i) in items" :key="i" :to="item.path">
              <v-list-item-icon>
                <v-icon v-text="item.icon"></v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title v-text="item.text"></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app clipped-left color="purple darken-4" dense dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>2020体育节成绩查询</v-toolbar-title>
    </v-app-bar>

    <v-main class="grey lighten-4">
        <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
export default {
  props: {
    source: String,
  },
  data: () => ({
    drawer: null,
    items: [
      { icon: "mdi-home", text: "主页", path: "/" },
      { icon: "mdi-trending-up", text: "成绩查询", path: "Query" },
    ],
  }),
  methods: {},
};
</script>