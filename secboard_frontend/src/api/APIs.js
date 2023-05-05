import requestAPI from "@/api/request";

const loginApi = (data) => {
	return requestAPI.post({
		url: "/login",
		data,
	});
};

const registerApi = (data) => {
	return requestAPI.post({
		url: "/register",
		data,
	});
};

const getPostsApi = (data) => {
	return requestAPI.post({
		url: "/getPosts",
		data,
	});
};

const makePost = (data) => {
	return requestAPI.post({
		url: "/makePost",
		data,
	});
};

export default { loginApi, registerApi, getPostsApi, makePost };
