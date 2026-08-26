import { useEffect, useRef, useState, type KeyboardEvent } from 'react';

interface RouteAutocompleteProps {
  routeNames: string[];
  value: string;
  onChange: (value: string) => void;
}

function RouteAutocomplete({ routeNames, value, onChange }: RouteAutocompleteProps) {
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [highlightIndex, setHighlightIndex] = useState(-1);
  const wrapperRef = useRef<HTMLDivElement>(null);

  const matches = value.trim() === ''
    ? routeNames
    : routeNames.filter((name) => name.includes(value.trim()));

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
      }
    }
    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, []);

  const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (!showSuggestions || matches.length === 0) return;
    if (event.key === 'ArrowDown') {
      event.preventDefault();
      setHighlightIndex((prev) => (prev + 1) % matches.length);
    } else if (event.key === 'ArrowUp') {
      event.preventDefault();
      setHighlightIndex((prev) => (prev - 1 + matches.length) % matches.length);
    } else if (event.key === 'Enter' && highlightIndex >= 0) {
      event.preventDefault();
      onChange(matches[highlightIndex]);
      setShowSuggestions(false);
    }
  };

  return (
    <div className="input-wrapper" ref={wrapperRef}>
      <input
        type="text"
        placeholder="例: 東名"
        autoComplete="off"
        value={value}
        onChange={(e) => {
          onChange(e.target.value);
          setShowSuggestions(true);
          setHighlightIndex(-1);
        }}
        onFocus={() => setShowSuggestions(true)}
        onKeyDown={handleKeyDown}
      />
      {showSuggestions && matches.length > 0 && (
        <ul className="suggestions">
          {matches.slice(0, 1000).map((name, idx) => (
            <li
              key={name}
              className={idx === highlightIndex ? 'highlighted' : ''}
              onClick={() => {
                onChange(name);
                setShowSuggestions(false);
              }}
            >
              {name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default RouteAutocomplete;
