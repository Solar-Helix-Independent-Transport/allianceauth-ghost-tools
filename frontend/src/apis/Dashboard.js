import axios from "axios";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

export async function loadDash() {
  const api = await axios.get(`api/ghost/list`);
  console.log(`get structure list in api`);
  console.log(api);
  return api.data;
}
