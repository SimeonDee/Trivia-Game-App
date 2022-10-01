import React, { Component } from 'react'
import $ from 'jquery';
import '../stylesheets/NewCategoryView.css'

export default class AddCategoryView extends Component {
  constructor(props) {
    super();
    this.state = {
      category_type: ''
    };
  }

  submitCategory = (event) => {
    event.preventDefault();
    $.ajax({
      url: '/categories', //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        type: this.state.category_type
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById('add-category-form').reset();
        if(result.message){
            alert(result.message)
        }
        else{
            alert('Category added')
        }
        return;
      },
      error: (error) => {
        alert('Unable to add category. Please try your request again');
        return;
      },
    });
  };

  handleChange = (event) => {
    this.setState({ category_type: event.target.value });
  };
  
    render() {
    return (
      <div>
        <h2>Add a New Trivia Category</h2>
        <form
          className='form-category-view'
          id='add-category-form'
          onSubmit={this.submitCategory}
        >
          <label>
            Category
            <input type='text' name='type' onChange={this.handleChange} />
          </label>
          <input type='submit' className='button' value='Add' />
        </form>
      </div>
    )
  }
}
