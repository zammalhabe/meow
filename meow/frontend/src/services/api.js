import axios from "axios";
import config from "../config";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.withCredentials = true;

const { SERVER_URL } = config;

export const themeList = () => {
  return axios
    .get(`${SERVER_URL}/users/themes/`, {
      withCredentials: true
    })
    .then(res => {
      return {
        data: res.data,
        status: res.status
      };
    });
};

<<<<<<< HEAD
export const additionalthemeList = () => {
  return axios.get(`${SERVER_URL}/users/additionalthemes/`).then(res => {
    return {
      data: res.data,
      status: res.status
    };
  });
};

export const starredthemesID = () => {
  return axios.get(`${SERVER_URL}/users/starredthemesID/`).then(res => {
    return {
      data: res.data,
      status: res.status
    };
  });
};

export const themeStarAdd = starredTheme => {
  return axios.post(`${SERVER_URL}/users/themeStar/`, starredTheme).then(res => {
    return {
      data: res.data,
      status: res.status
    };
  });
};

export const themeStarRemove = starredTheme => {
  return axios.put(`${SERVER_URL}/users/themeStar/`, starredTheme).then(res => {
    return {
      data: res.data,
      status: res.status
    };
  });
};

export const themeAdd = newTheme => {
  return axios.post(`${SERVER_URL}/users/themeAdd/`, newTheme).then(res => {
    return {
      data: res.data,
      status: res.status
    };
  });
};

export const themeEdit = updatedTheme => {
  return axios.put(`${SERVER_URL}/users/themeEdit/`, updatedTheme).then(res => {
    return {
      data: res.data,
      status: res.status
    };
  });
};

export const themeDelete = deletedTheme => {
  return axios.put(`${SERVER_URL}/users/themeDelete/`, deletedTheme).then(res => {
    return {
      data: res.data,
      status: res.status
    };
  });
=======
export const themeAdd = newTheme => {
<<<<<<< HEAD
  return axios.post(`${SERVER_URL}/users/themeAdd/`, newTheme);
>>>>>>> Added theme color dial in the frontend, added new themeAdd view in views.py
=======
  return axios.post(`${SERVER_URL}/users/themeAdd/`, newTheme).then(res => ({
    data: res.data,
    status: res.status
  }));
};

export const themeEdit = updatedTheme => {
  return axios.put(`${SERVER_URL}/users/themeEdit/`, updatedTheme).then(res => ({
    data: res.data,
    status: res.status
  }));
};

export const themeDelete = deletedTheme => {
  return axios.put(`${SERVER_URL}/users/themeDelete/`, deletedTheme).then(res => ({
    data: res.data,
    status: res.status
  }));
>>>>>>> Implemented theme add, theme delete and theme update functions in views.py of user profile
};

export const getMe = () => {
  return axios
    .get(`${SERVER_URL}/users/me/`, {
      withCredentials: true
    })
    .then(res => {
      return {
        data: res.data,
        status: res.status
      };
    });
};

export const logout = () => {
  return axios
    .get(`${SERVER_URL}/users/logout/`, {
      withCredentials: true
    })
    .then(res => {
      return {
        status: res.status
      };
    });
};

export const userDetail = username => {
  return axios
    .get(`${SERVER_URL}/users/${username}`, {
      withCredentials: true
    })
    .then(res => {
      return res;
    });
};

export const putUser = newData => {
  return axios.put(`${SERVER_URL}/users/me/`, newData).then(res => ({
    data: res.data,
    status: res.status
  }));
};

export const postList = YMD => {
  return axios
    .get(`${SERVER_URL}/post/?year=${YMD.year}&month=${YMD.month}&day=${YMD.day}`, {
      withCredentials: true
    })
    .then(res => ({
      data: res.data,
      status: res.status
    }));
};

export const postDetail = postId => {
  return axios
    .get(`${SERVER_URL}/post/${postId}`, {
      withCredentials: true
    })
    .then(res => ({
      data: res.data,
      status: res.status
    }));
};

export const getTagSuggestions = () => {
  return axios.get(`${SERVER_URL}/tags/suggestions`).then(res => ({
    data: res.data,
    status: res.status
  }));
};

const postTags = postData => {
  if (postData !== undefined && postData.tags !== undefined) {
    //return promise with no then we we can easily hook it together in the chain.
    return axios.post(`${SERVER_URL}/tags/create-many`, postData.tags);
  }
  return Promise.resolve();
};

export const postPost = (postId, postData) => {
  //first inspect the data to see if we have tags
  //they will be formated as an array of strings

  if (postId) {
    return postTags(postData).then(() =>
      axios.put(`${SERVER_URL}/post/${postId}`, postData).then(res => ({
        data: res.data,
        status: res.status
      }))
    );
  }

  return postTags(postData).then(() =>
    axios.post(`${SERVER_URL}/post/`, postData).then(res => ({
      data: res.data,
      status: res.status
    }))
  );
};

export const postSendNow = postId => {
  return axios.post(`${SERVER_URL}/post/${postId}/send_now`);
};

export const sectionList = () => {
  return axios
    .get(`${SERVER_URL}/section/`, {
      withCredentials: true
    })
    .then(res => ({
      data: res.data,
      status: res.status
    }));
};

export const getHistory = postId =>
  axios.get(`${SERVER_URL}/history/${postId}`).then(({ data, status }) => ({
    data,
    status
  }));
