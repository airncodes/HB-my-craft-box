function TagButton(props) {
    return (
        <button type="button" className="btn toggle-btn" aria-pressed={props.isPressed} onClick={() => props.setFilter(props.tag)}>
            <span className="visually-hidden"></span>
            <span>{props.tag}</span>
            <span className="visually-hidden"></span>
        </button>
      );
  }


function ButtonContainer() {
    const [buttons, setTagButtons] = React.useState([]);
    
    function addButton() {
        
        const currentButtons = [...buttons]; 
        setTagButtons([...currentButtons]);
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
            <div>{tagButtons}</div>
        </React.Fragment>
    );
}

ReactDOM.render(<ButtonContainer/>, document.querySelector('#buttoncontainer'));
