function LinkCard(props) {
    return (
      <div className="link">
        <img src={props.image} alt="profile" />
        <a href="{props.link_path}">{props.name}</a>
        <p> Notes: {props.notes} </p>
      </div>
    );
  }



{/* <h2>Links Added</h2> 
    <ul>
    {% for link in links %}
    
    <li><a href="{{link.link_path}}">{{link.name}}</a></li>
    
    {% endfor %}
    </ul> */}