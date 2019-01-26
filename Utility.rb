class Utility
  def self.which(binary)
    ENV["PATH"].split(File::PATH_SEPARATOR).map do |path|
      path = File.join(path, binary)
      return path if File.exists?(path) and File.executable?(path)
    end.uniq.first
  end
end
