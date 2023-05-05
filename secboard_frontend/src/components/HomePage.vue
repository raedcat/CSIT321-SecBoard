<template>
	<div>
		<h1>I'M HOME PAGE</h1>
	</div>
	<div>
		<h3>My name: {{ name }}</h3>
		<h3>My email: {{ email }}</h3>
		<h3>My token:</h3>
		<h3>{{ token.token }}</h3>
	</div>

	<div style="margin-left: 50px">
		<div style="margin-top: 30px">
			<el-button type="success" @click="makePost">Make a post</el-button>
			<el-button @click="refreshTable">Refresh</el-button>
		</div>
		<div>
			<el-table :data="postsList" height="250" style="width: 100%">
				<el-table-column prop="user_name" label="Name" width="180" />
				<el-table-column prop="content" label="Content" width="180" />
			</el-table>
		</div>
	</div>
</template>

<script setup>
import { reactive, ref } from "vue";
import api from "@/api/APIs";
import { ElMessage, ElMessageBox } from "element-plus";

const name = ref(window.sessionStorage.getItem("name"));
const email = ref(window.sessionStorage.getItem("email"));
const token = reactive({
	token: window.sessionStorage.getItem("token"),
});

const postsList = ref([]);

api.getPostsApi(token).then((res) => {
	postsList.value = res.posts;
});

const postForm = reactive({
	name: window.sessionStorage.getItem("name"),
	content: "",
	token: window.sessionStorage.getItem("token"),
});
function makePost() {
	ElMessageBox.prompt("Enter content", "Make a post", {
		confirmButtonText: "Post",
		cancelButtonText: "Cancel",
	})
		.then(({ value }) => {
			postForm.content = value;
			console.log(postForm.name);
			api.makePost(postForm).then((res) => {
				if (res.status === 201) {
					api.getPostsApi(token).then((res) => {
						postsList.value = res.posts;
					});
					ElMessage({
						type: "success",
						message: "DONE!",
					});
				} else {
					ElMessage({
						type: "warning",
						message: "Something wrong!",
					});
				}
			});
		})
		.catch(() => {
			ElMessage({
				type: "info",
				message: "Input canceled",
			});
		});
}

function refreshTable() {
	api.getPostsApi(token).then((res) => {
		postsList.value = res.posts;
	});
}
</script>
