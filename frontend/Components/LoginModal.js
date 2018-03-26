import React from "react";
import Modal from 'material-ui-next/Modal';
import PropTypes from 'prop-types';
import Typography from 'material-ui-next/Typography';
import Tabs, { Tab } from 'material-ui-next/Tabs';
import { withStyles } from 'material-ui-next/styles';
import Input, { InputLabel } from 'material-ui-next/Input';
import TextField from 'material-ui-next/TextField';
import { FormControl } from 'material-ui-next/Form';
import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';

const styles = theme => ({
  paper: {
    position: 'absolute',
    backgroundColor: theme.palette.background.paper,
    boxShadow: theme.shadows[5],
    padding: theme.spacing.unit * 4,
  }
});

class LoginModal extends React.Component {
  state = {
    open: '',
    value: '0',
    loginForm: 'block',
    registerForm: 'none',
    modalWidth: '400px'
  }

  componentDidMount() {
    window.addEventListener("resize", this.resize.bind(this));
    this.resize();
  }

  resize() {
    this.setState({modalWidth: window.innerWidth <= 760 ? '90%' : '400px'});
  }

  componentWillReceiveProps = (nextProps) => {
      if((nextProps.clicked == '0') || (nextProps.clicked == '1')){
          this.setState({value: nextProps.clicked, open: true})
      }
  }

  handleClose = () => {
    this.setState({ open: ''});
    this.props.onClose();
  };

  changeDisplay = () => {
    if(this.state.value == 0){
      this.setState({loginForm: 'block', registerForm: 'none'})
    }
    else if(this.state.value == 1){
      this.setState({loginForm: 'none', registerForm: 'block'});
    }
  }

  handleTabChange = (event, value) => {
    this.setState({ value }, function(){
      this.changeDisplay();
    })
  }

  handleLogin = () => {
    this.setState({open: ''});
    this.props.loggedIn();
  }

  handleRegister = () => {
    this.setState({open: ''});
    this.props.registered();
  }

  render() {
    const { classes } = this.props;

    return (
      <div>
        <Modal
          style={{justifyContent: 'center', alignItems: 'center'}}
          aria-labelledby="simple-modal-title"
          aria-describedby="simple-modal-description"
          open={this.state.open}
          onClose={this.handleClose}
          onRendered={this.changeDisplay}
        >
          <div className={classes.paper} style={{width: this.state.modalWidth}}>
            <Tabs
              value={this.state.value}
              indicatorColor="primary"
              textColor="primary"
              onChange={this.handleTabChange}
              fullWidth
            >
              <Tab label="Login" />
              <Tab label="Register" />
            </Tabs>
              <LoginForm display={this.state.loginForm} loggedIn={this.handleLogin}/>
              <RegisterForm display={this.state.registerForm} registered={this.handleRegister}/>
          </div>
        </Modal>
      </div>
    );
  }
}

const LoginModalWrapped = withStyles(styles)(LoginModal);

export default LoginModalWrapped;
