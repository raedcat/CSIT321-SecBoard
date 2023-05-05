const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
	transpileDependencies: true,
	filenameHashing: true,
	productionSourceMap: false,
});

module.exports = {
	productionSourceMap: false,
};

module.exports = {
	devServer: {
		proxy: {
			"/api": {
				target: "http://10.12.162.234:3210",
				changeOrigin: true,
				pathRewrite: {
					"^/api": "api",
				},
			},
		},
	},
};
