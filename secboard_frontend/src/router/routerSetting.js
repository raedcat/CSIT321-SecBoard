// import { createRouter, createWebHistory } from 'vue-router'

import { createRouter, createWebHistory } from "vue-router";
const loginPage = () => import("../components/LoginPage");
const registerPage = () => import("../components/RegisterPage");
const homePage = () => import("../components/HomePage");

const router = createRouter({
	history: createWebHistory(),
	routes: [
		{
			path: "/",
			redirect: "login",
		},
		{
			path: "/login",
			name: "login",
			component: loginPage,
		},
		{
			path: "/register",
			name: "register",
			component: registerPage,
		},
		{
			path: "/home",
			name: "home",
			component: homePage,
		},
	],
});

export default router;
