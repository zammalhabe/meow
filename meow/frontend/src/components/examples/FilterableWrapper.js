import React from 'react';
import axios from 'axios';
import PostGetter from './PostGetter';
import Sidebar from '../Sidebar/Sidebar';

const ENDPOINT = '/api/post/';

export default class FilterableWrapper extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      posts: [],
      filteredPosts: [],
      gt2: false
    };
    this.handleToggle = this.handleToggle.bind(this);
  }

  componentDidMount() {
    axios.get(ENDPOINT).then(res => {
      this.setState({ posts: res.data, filteredPosts: res.data });
    });
  }

  handleToggle() {
    let filtered = !this.state.gt2;
    let newPosts = filtered
      ? this.state.posts.filter(post => {
          return post.id > 2;
        })
      : this.state.posts;
    this.setState({ filteredPosts: newPosts, gt2: filtered });
  }

  render() {
    const posts = this.state.filteredPosts;

    return (
      <div>
        <Sidebar />
        <PostGetter posts={posts} />
      </div>
    );
  }
}