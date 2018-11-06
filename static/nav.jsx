

"use strict";

class Nav extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return <span> { this.props.item } </span>;
  }
}

class NavList extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        console.log(this.props.items);
        const navs = [];
        for (let item of this.props.items) {
            navs.push(<Nav item={item} />)
        }

        return navs;
    }
}


ReactDOM.render(
  (
    <div>
      <Nav item="Salary table" />
      <Nav item="Google trends" />
      <Nav item="Job listings" />
    </div>
  ),
  document.getElementById('navbar')
);


