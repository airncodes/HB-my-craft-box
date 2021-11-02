function TagButton(props) {
    const tag = props.tag;
    
    function filterCard() {
        fetch('/craftboxr.json', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({tag}),
          }).then(response => {
            console.log(response)
          });
    }
    
    return (
        <button id={props.tag} type="button" className="btn toggle-btn" aria-pressed={props.isPressed} onClick={filterCard}>
            <span>{props.tag}</span>
            <input  type="text" name="tag" defaultValue={props.tag} hidden></input>
        </button>
      );
} 

function ButtonContainer(props) {
    const [buttons, setTagButtons] = React.useState([]);
    
    function addButton() {
        setTagButtons(...currentButtons);
    }

    React.useEffect(() => {
        fetch('/craftboxb.json')
            .then(response => response.json())
            .then(data => setTagButtons(data.buttons));
    }, []);

    const tagButtons = [];

    console.log(`tagButtons: `, tagButtons);
    
    
    
    
    for (const currentButton of buttons) {
        tagButtons.push(
        <TagButton addButton={addButton}
            tag={currentButton.tag}
        />
        );
    }
    
    console.log(`tagButtons: `, tagButtons);
    
    

    return (
        <React.Fragment>
            <h2>Filter Search</h2>
            <div>{tagButtons}</div>
        </React.Fragment>
    );
}

ReactDOM.render(<ButtonContainer/>, document.querySelector('#buttoncontainer'));
