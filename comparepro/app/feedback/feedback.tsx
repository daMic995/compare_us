// For more help visit https://formspr.ee/react-help
import React from 'react';
import { useForm, ValidationError } from '@formspree/react';

function ContactForm() {
  const [state, handleSubmit] = useForm("xgvoyqyw");
  if (state.succeeded) {
      return <p>Thanks for your feedback!</p>;
  }
  return (
    <form onSubmit={handleSubmit} className='flex flex-col w-3/4'>
      <div className='flex flex-col mb-4 w-1/2'>
        <label htmlFor="name" className='mb-2'>
          Name
        </label>
        <input id="name" name="name" placeholder='John Doe' 
        className='p-2 border border-gray-300 rounded-lg mb-2'/>
        <ValidationError prefix="Name" field="name"
          errors={state.errors}
        />
      </div>
      <div className='flex flex-col mb-2'>
        <label htmlFor="email" className='mb-2'>
          E-mail
        </label>
        <input id="email" type="email" name="email" required
        placeholder='myname@example.com' className='p-2 border border-gray-300 rounded-lg mb-2'/>
        <ValidationError prefix="Email" field="email"
          errors={state.errors}
        />
      </div>
      <div className='flex mb-2 lg:mb-8 text-sm'>
        <label className='mr-4'>
          <input type="radio" name="feedback-type" value="Comments" defaultChecked/> Comments
        </label>
        <label className='mr-4'>
          <input type="radio" name="feedback-type" value="Suggestions"/> Suggestions
        </label>
        <label className='mr-4'>
          <input type="radio" name="feedback-type" value="Problems/Questions"/> Questions
        </label>
        <ValidationError prefix="Feedback-Type" field="feedback-type"
          errors={state.errors}
        />
      </div>
      <div className='flex flex-col mb-2'>
        <label htmlFor="message" className='mb-2'>
          Describe your Feedback:
        </label>
        <textarea id="message" name="message" required
        className='p-2 border border-gray-300 rounded-lg mb-2 h-32'/>
        <ValidationError prefix="Message" field="message"
          errors={state.errors}
        />
      </div>
      <div className='flex flex-col items-center'>
      <button type="submit" className='bg-black hover:bg-blue-500 text-white py-2 w-1/2 rounded-lg focus:shadow-outline focus:outline-none transition duration-300 ease-in-out' disabled={state.submitting}>
        Submit
      </button>
      </div>
    </form>
  );
}

export default ContactForm;