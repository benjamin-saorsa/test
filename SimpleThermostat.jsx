import React, { useState, useEffect } from 'react';
import { Thermometer, Plus, Minus, Power, Flame, Snowflake } from 'lucide-react';

export default function SimpleThermostat() {
  const [targetTemp, setTargetTemp] = useState(72);
  const [currentTemp, setCurrentTemp] = useState(68);
  const [isOn, setIsOn] = useState(true);
  const [mode, setMode] = useState('auto'); // 'heat', 'cool', 'auto', 'off'
  const [isHeating, setIsHeating] = useState(false);
  const [isCooling, setIsCooling] = useState(false);
  const [isCelsius, setIsCelsius] = useState(false);

  // Temperature conversion functions
  const fahrenheitToCelsius = (f) => Math.round(((f - 32) * 5/9) * 10) / 10;
  const celsiusToFahrenheit = (c) => Math.round((c * 9/5 + 32) * 10) / 10;
  
  const displayTemp = (temp, isTarget = false) => {
    if (isCelsius) {
      const converted = fahrenheitToCelsius(temp);
      return isTarget ? Math.round(converted) : converted;
    }
    return isTarget ? Math.round(temp) : temp;
  };
  
  const getMinMaxTemp = () => {
    if (isCelsius) {
      return { min: 10, max: 32 }; // 50°F to 90°F in Celsius
    }
    return { min: 50, max: 90 };
  };

  // Simulate temperature changes
  useEffect(() => {
    if (!isOn) return;

    const interval = setInterval(() => {
      setCurrentTemp(prevTemp => {
        let newTemp = prevTemp;
        
        if (mode === 'heat' || (mode === 'auto' && prevTemp < targetTemp - 1)) {
          setIsHeating(true);
          setIsCooling(false);
          newTemp = Math.min(prevTemp + 0.5, targetTemp);
        } else if (mode === 'cool' || (mode === 'auto' && prevTemp > targetTemp + 1)) {
          setIsHeating(false);
          setIsCooling(true);
          newTemp = Math.max(prevTemp - 0.5, targetTemp);
        } else {
          setIsHeating(false);
          setIsCooling(false);
          // Natural temperature drift
          const drift = (Math.random() - 0.5) * 0.2;
          newTemp = prevTemp + drift;
        }
        
        return Math.round(newTemp * 10) / 10;
      });
    }, 2000);

    return () => clearInterval(interval);
  }, [targetTemp, mode, isOn]);

  const adjustTemp = (delta) => {
    const { min, max } = getMinMaxTemp();
    const currentDisplayTemp = displayTemp(targetTemp, true);
    const newDisplayTemp = Math.max(min, Math.min(max, currentDisplayTemp + delta));
    
    if (isCelsius) {
      setTargetTemp(celsiusToFahrenheit(newDisplayTemp));
    } else {
      setTargetTemp(newDisplayTemp);
    }
  };

  const togglePower = () => {
    setIsOn(!isOn);
    if (isOn) {
      setIsHeating(false);
      setIsCooling(false);
    }
  };

  const toggleTempUnit = () => {
    setIsCelsius(!isCelsius);
  };

  const getStatusColor = () => {
    if (!isOn) return 'text-gray-400';
    if (isHeating) return 'text-red-500';
    if (isCooling) return 'text-blue-500';
    return 'text-green-500';
  };

  const getStatusText = () => {
    if (!isOn) return 'Off';
    if (isHeating) return 'Heating';
    if (isCooling) return 'Cooling';
    return 'Idle';
  };

  return (
    <div className="max-w-md mx-auto mt-8 p-8 bg-gradient-to-br from-slate-900 to-slate-800 rounded-3xl shadow-2xl text-white">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="flex items-center justify-center gap-2 mb-2">
          <Thermometer className="w-6 h-6" />
          <h1 className="text-2xl font-bold">Smart Thermostat</h1>
          <button
            onClick={toggleTempUnit}
            className="ml-2 px-2 py-1 text-xs bg-gray-700 hover:bg-gray-600 rounded transition-colors"
          >
            °{isCelsius ? 'C' : 'F'}
          </button>
        </div>
        <div className={`text-sm font-medium ${getStatusColor()}`}>
          {getStatusText()}
        </div>
      </div>

      {/* Current Temperature Display */}
      <div className="text-center mb-8">
        <div className="text-6xl font-light mb-2">
          {displayTemp(currentTemp)}°
        </div>
        <div className="text-gray-400 text-sm">Current Temperature</div>
      </div>

      {/* Target Temperature Controls */}
      <div className="flex items-center justify-center gap-4 mb-8">
        <button
          onClick={() => adjustTemp(-1)}
          disabled={!isOn}
          className="w-12 h-12 rounded-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed flex items-center justify-center transition-colors"
        >
          <Minus className="w-6 h-6" />
        </button>
        
        <div className="text-center">
          <div className="text-3xl font-bold mb-1">{displayTemp(targetTemp, true)}°</div>
          <div className="text-gray-400 text-xs">Target</div>
        </div>
        
        <button
          onClick={() => adjustTemp(1)}
          disabled={!isOn}
          className="w-12 h-12 rounded-full bg-red-600 hover:bg-red-700 disabled:bg-gray-600 disabled:cursor-not-allowed flex items-center justify-center transition-colors"
        >
          <Plus className="w-6 h-6" />
        </button>
      </div>

      {/* Mode Selection */}
      <div className="flex gap-2 mb-6">
        {['heat', 'cool', 'auto'].map((modeOption) => (
          <button
            key={modeOption}
            onClick={() => setMode(modeOption)}
            disabled={!isOn}
            className={`flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-colors ${
              mode === modeOption && isOn
                ? 'bg-blue-600 text-white'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            } disabled:bg-gray-800 disabled:text-gray-500 disabled:cursor-not-allowed`}
          >
            <div className="flex items-center justify-center gap-1">
              {modeOption === 'heat' && <Flame className="w-4 h-4" />}
              {modeOption === 'cool' && <Snowflake className="w-4 h-4" />}
              {modeOption.charAt(0).toUpperCase() + modeOption.slice(1)}
            </div>
          </button>
        ))}
      </div>

      {/* Power Button */}
      <button
        onClick={togglePower}
        className={`w-full py-4 rounded-xl font-semibold transition-all duration-300 flex items-center justify-center gap-2 ${
          isOn
            ? 'bg-red-600 hover:bg-red-700 text-white'
            : 'bg-green-600 hover:bg-green-700 text-white'
        }`}
      >
        <Power className="w-5 h-5" />
        {isOn ? 'Turn Off' : 'Turn On'}
      </button>

      {/* Status Indicators */}
      <div className="flex justify-center gap-4 mt-6">
        <div className={`flex items-center gap-1 text-sm ${isHeating ? 'text-red-400' : 'text-gray-500'}`}>
          <Flame className="w-4 h-4" />
          <span>Heat</span>
        </div>
        <div className={`flex items-center gap-1 text-sm ${isCooling ? 'text-blue-400' : 'text-gray-500'}`}>
          <Snowflake className="w-4 h-4" />
          <span>Cool</span>
        </div>
      </div>
    </div>
  );
}