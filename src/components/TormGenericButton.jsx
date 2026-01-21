import { useNavigate } from "react-router-dom";
import "../styles/TormGenericBtnStyle.css"

const TormGenericButton = ({ btnIcon, title, path, onClick }) => {
  const navigate = useNavigate();

  const handleClick = (e) => {
    if (path) {
      navigate(path);
      return;
    }

    if (onClick) {
      onClick(e);
    }
  };

  return (
    <button className="torm-button" onClick={handleClick}>
      {btnIcon && <span className="btn-icon">{btnIcon}</span>}
      <span className="btn-title">{title}</span>
    </button>
  );
};

export default TormGenericButton;