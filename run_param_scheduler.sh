#!/bin/bash

# Define o número inicial de salas e o incremento
initial_rooms=10
increment=10
max_rooms=10000 # Defina o valor máximo que você deseja para o número de salas

python_script="scheduler.py"

log_dir="scheduler_logs"
mkdir -p "$log_dir"

current_rooms=$initial_rooms
while [ $current_rooms -le $max_rooms ]; do
  log_file="$log_dir/scheduler_${current_rooms}.log"

  # Executa o script Python e aguarda a conclusão
  echo "Executando com $current_rooms salas. Saída será salva em $log_file"
  python3 "$python_script" "$current_rooms" >"$log_file" 2>&1

  # Verifica se a execução foi bem-sucedida
  if [ $? -eq 0 ]; then
    echo "Execução com $current_rooms salas concluída com sucesso."
  else
    echo "Erro na execução com $current_rooms salas. Verifique $log_file para detalhes."
    break
  fi

  current_rooms=$((current_rooms + increment))
done

echo "Todas as execuções foram concluídas ou interrompidas devido a um erro."