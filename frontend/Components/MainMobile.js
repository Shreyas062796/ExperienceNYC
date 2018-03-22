import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui-next/styles';
import Card, { CardActions, CardContent } from 'material-ui-next/Card';
import classNames from 'classnames';
import Grid from 'material-ui-next/Grid';
import BottomNav from './BottomNav';
import AppBar from 'material-ui-next/AppBar';
import Toolbar from 'material-ui-next/Toolbar';
import List from 'material-ui-next/List';
import Typography from 'material-ui-next/Typography';
import TextField from 'material-ui-next/TextField';
import Divider from 'material-ui-next/Divider';
import IconButton from 'material-ui-next/IconButton';
import MenuIcon from 'material-ui-icons/Menu';
import ChevronLeftIcon from 'material-ui-icons/ChevronLeft';
import ChevronRightIcon from 'material-ui-icons/ChevronRight';
import Place from 'material-ui-icons/Place';
import FilterBar from './FilterBar';
import Cards from './Cards';
import Button from 'material-ui-next/Button';
import LoginModal from './LoginModal';
import AccountCircle from 'material-ui-icons/AccountCircle';
import Menu, { MenuItem } from 'material-ui-next/Menu';
import Trips from './Trips.js';

const styles = theme => ({
  root: {
    flexGrow: 1,
  },
  appFrame: {
    zIndex: 1,
    overflow: 'hidden',
    width: '100%',
  },
  appBar: {
    position: 'absolute'
  },
  menuButton: {
    marginLeft: -12,
    marginRight: 20,
  }
});

class Main extends React.Component {
  constructor(props){
    super(props)

    this.handlePage = this.handlePage.bind(this)
  }
  state = {
    clicked: '',
    username: '',
    anchorEl: null,
    currentPage: 'search'
  };

  handleLoginClick = () => {
    this.setState({clicked: 0});
  }

  handleRegisterClick = () => {
    this.setState({clicked: 1});
  }

  handleMenu = event => {
    this.setState({ anchorEl: event.currentTarget });
  };

  handleClose = () => {
    this.setState({ anchorEl: null });
  };

  handlePage = (page) => {
    this.setState({
      currentPage: page
    })
  }

  handleModalClose = () => {
    this.setState({clicked: ''})
  }

  handleLogin = () => {
    this.setState({username: sessionStorage.getItem('username'), loginClick: ''})
  }

  handleLogout = () => {
    this.setState({username: ''})
    sessionStorage.setItem('username', '')
    alert("Logged Out!")
  }

  handlePageDisplay = (page) => {
    if(page == this.state.currentPage){
      return 'block';
    }
    else{
      return 'none';
    }
  }

  render() {
    const { classes, theme  } = this.props;
    const { username, anchorEl } = this.state;

    const menuOpen = Boolean(anchorEl);

    let userAppbarOption = null;

    if(this.state.username){
      userAppbarOption = (<div><Typography style={{color: 'white', display: 'inline-block'}}>{this.state.username}</Typography><IconButton
                            aria-owns={menuOpen ? 'menu-appbar' : null}
                            aria-haspopup="true"
                            onClick={this.handleMenu}
                          >
                            <AccountCircle color="white"/>
                          </IconButton>
                          <Menu
                            id="menu-appbar"
                            anchorEl={anchorEl}
                            anchorOrigin={{
                              vertical: 'top',
                              horizontal: 'right',
                            }}
                            transformOrigin={{
                              vertical: 'top',
                              horizontal: 'right',
                            }}
                            open={menuOpen}
                            onClose={this.handleClose}
                          >
                            <MenuItem onClick={this.handleClose}>Profile</MenuItem>
                            <MenuItem onClick={this.handleClose}>My account</MenuItem>
                            <MenuItem onClick={this.handleLogout}>Logout</MenuItem>
                          </Menu></div>);
    }
    else {
      userAppbarOption = (<Typography style={{color: 'white', cursor: 'pointer'}}>
                            <a onClick={this.handleLoginClick}>Login</a> | <a onClick={this.handleRegisterClick}>Signup</a>
                          </Typography>);

    }

    return (
      <div className={classes.root}>
        <div className={classes.appFrame}>
          <AppBar
            className={classes.appBar}

          >
            <Toolbar disableGutters={!open}>
              <div style={{width: '50%'}}>
                <Typography variant="title" color="inherit" noWrap>
                  Experience NYC
                </Typography>
              </div>
              <div style={{width: '50%', alignItems: 'center', justifyContent: 'flex-end', display: 'flex'}}>
                {userAppbarOption}
              </div>
            </Toolbar>

          </AppBar>
          <div style={{display: this.handlePageDisplay('search')}}>
            <FilterBar />
              <LoginModal
                clicked={this.state.clicked}
                onClose={this.handleModalClose}
              />
            <Cards />
          </div>
          <div style={{display: this.handlePageDisplay('favorites')}}>

          </div>
          <div style={{display: this.handlePageDisplay('trips')}}>
            <Trips />
          </div>
          <BottomNav pageChange={this.handlePage}/>
        </div>
      </div>
    );
  }
}

Main.propTypes = {
  classes: PropTypes.object.isRequired,
  theme: PropTypes.object.isRequired,
};

export default withStyles(styles, { withTheme: true })(Main);
