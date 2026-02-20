#!/usr/bin/env ruby

require "yaml"

ROOT = File.expand_path("..", __dir__)
AGENTS_DIR = File.join(ROOT, "agents")

def extract_frontmatter(path)
  content = File.read(path)
  lines = content.lines

  return nil unless lines.first&.strip == "---"

  closing_idx = lines[1..]&.find_index { |line| line.strip == "---" }
  return nil unless closing_idx

  lines[1..closing_idx].join
end

def err(errors, path, message)
  errors << "#{path}: #{message}"
end

errors = []
files = Dir.glob(File.join(AGENTS_DIR, "**", "*.md")).sort
files.reject! { |path| File.basename(path).casecmp("README.md").zero? }

if files.empty?
  warn "No agent files found under #{AGENTS_DIR}"
  exit 1
end

files.each do |path|
  frontmatter = extract_frontmatter(path)
  if frontmatter.nil?
    err(errors, path, "missing or malformed YAML frontmatter")
    next
  end

  parsed = begin
    YAML.safe_load(frontmatter, permitted_classes: [], aliases: false)
  rescue Psych::SyntaxError => e
    err(errors, path, "invalid YAML: #{e.message.lines.first.strip}")
    next
  end

  unless parsed.is_a?(Hash)
    err(errors, path, "frontmatter must be a mapping/object")
    next
  end

  name = parsed["name"]
  description = parsed["description"]
  tools = parsed["tools"]
  model = parsed["model"]

  if !name.is_a?(String) || name.strip.empty?
    err(errors, path, "`name` must be a non-empty string")
  end

  if !description.is_a?(String) || description.strip.empty?
    err(errors, path, "`description` must be a non-empty string")
  end

  unless tools.is_a?(Hash)
    err(errors, path, "`tools` must be an object/map of toolName: boolean")
    next
  end

  if tools.empty?
    err(errors, path, "`tools` must not be empty")
  end

  tools.each do |tool_name, enabled|
    if !tool_name.is_a?(String) || tool_name.strip.empty?
      err(errors, path, "tool keys in `tools` must be non-empty strings")
    end

    unless enabled == true || enabled == false
      err(errors, path, "tool `#{tool_name}` must be boolean (true/false)")
    end
  end

  if parsed.key?("model") && !model.is_a?(String)
    err(errors, path, "`model` must be a string when present")
  end
end

if errors.empty?
  puts "Agent validation passed (#{files.length} files)"
  exit 0
end

warn "Agent validation failed:"
errors.each { |e| warn "- #{e}" }
exit 1
