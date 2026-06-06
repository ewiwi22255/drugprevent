<template>
    <div class="input-group">
        <input 
            type="text" 
            class="form-control" 
            placeholder="請輸入您想說的話..." 
            :value="modelValue"
            @input="$emit('update:modelValue', $event.target.value)"
            @keyup.enter="!disabled && $emit('send')"
        >
        <button 
            class="btn btn-primary" 
            type="button" 
            @click="$emit('send')" 
            :disabled="disabled"
        >
            送出
        </button>
    </div>
</template>

<script>
export default {
    name: 'WordsInput',
    props: {
        modelValue: String,
        disabled: Boolean
    },
    emits: ['update:modelValue', 'send']
}
</script>