import React, { Component } from 'react';
import { browserHistory } from 'react-router';
import { Layout, Menu, Breadcrumb, Icon, Dropdown, Badge } from 'antd';
import NProgress from 'nprogress';
import style from 'styles/App.css';

const { SubMenu } = Menu;
const MenuItemGroup = Menu.ItemGroup;
const { Header, Content, Sider } = Layout;

const breadCrumbMap = {
  '/': ['Home'],
  '/config/user/list': ['Home', '用户中心', '用户列表'],
  '/config/user/add': ['Home', '用户中心', '添加用户'],
  '/config/user/edit': ['Home', '用户中心', '编辑用户'],
  '/config/role/list': ['Home', '用户中心', '角色列表'],
  '/config/role/add': ['Home', '用户中心', '添加角色'],
  '/config/role/edit': ['Home', '用户中心', '编辑角色'],
}

class App extends Component {

  constructor(...args) {
    super(...args);
    this.state = {
      current: '/',
    };
  }

  componentDidMount() {
      NProgress.done();
  }

  handleClick = (e) => {
      const key = e.key;
      this.setState({
          current: key,
      });
      browserHistory.push(key);
  }

  render() {
    const menu = (
      <Menu>
        <Menu.Item>
          <a rel="noopener noreferrer" href="#">退出</a>
        </Menu.Item>
      </Menu>
    );

    const { current } = this.state;    

    return (
      <Layout>
        <Header className="header">
          <div className="logo" />
          <Menu
            theme="dark"
            mode="horizontal"
            style={{ lineHeight: '64px' }}
            onClick={this.handleClick}
          >
            <Dropdown overlay={menu} trigger={['click']}>
              <a className={`${style.dropDown} ant-dropdown-link pull-right`}>
                瓦力用户 <Icon type="down" />
              </a>
            </Dropdown>
            <Menu.Item key="/message" style={{float: 'right'}}>
              <Badge dot>
                <Icon type="message" />
              </Badge>
            </Menu.Item>
          </Menu>
        </Header>
        <Layout>
          <Sider width={200} style={{ background: '#fff' }}>
            <Menu
              mode="inline"
              defaultOpenKeys={['sub1']}
              style={{ height: '100%' }}
              onClick={this.handleClick}
            >
              <SubMenu key="config" title={<span><Icon type="user" />用户中心</span>}>
                <MenuItemGroup key="user" title="用户管理">
                  <Menu.Item key="/config/user/list">用户列表</Menu.Item>
                  <Menu.Item key="/config/user/add">添加用户</Menu.Item>
                </MenuItemGroup>
                <MenuItemGroup key="role" title="角色管理">
                  <Menu.Item key="/config/role/list">角色列表</Menu.Item>
                  <Menu.Item key="/config/role/add">添加角色</Menu.Item>
                </MenuItemGroup>
              </SubMenu>
              <SubMenu key="project" title={<span><Icon type="laptop" />项目管理</span>}>
                <Menu.Item key="5">option5</Menu.Item>
                <Menu.Item key="6">option6</Menu.Item>
                <Menu.Item key="7">option7</Menu.Item>
                <Menu.Item key="8">option8</Menu.Item>
              </SubMenu>
            </Menu>
          </Sider>
          <Layout style={{ padding: '0 24px 24px' }}>
            <Breadcrumb style={{ margin: '12px 0' }}>
              { breadCrumbMap[current].map(item => (<Breadcrumb.Item>{item}</Breadcrumb.Item>)) }
            </Breadcrumb>
            <Content style={{ background: '#fff', padding: 24, margin: 0, minHeight: 280 }}>
              {this.props.children}
            </Content>
          </Layout>
        </Layout>
      </Layout>
    );
  }
}

export default App;